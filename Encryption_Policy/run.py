from antlr4 import *
from epLexer import epLexer
from epListener import epListener
from epParser import epParser
from epVisitor import epVisitor
import sys
import binascii
from collections import defaultdict
from ndn.encoding import *
from itertools import product

idDict = {}
defDict = defaultdict(list)
expandDict = defaultdict(list)
tempDict = {}
KEKDict = defaultdict(list)

tokenDict = {}
certDict = {}
consDict = defaultdict(list)
tagDict = {}
tempList = []
chainList = []
pubList = []

parentList = set()
childList = []
literalList = []
primary = []
parent = defaultdict(list)
children = {}
cons = {}
signer = defaultdict(list)
tempChain = []
tempChainDic = defaultdict(list)


class NestedModel(TlvModel):
    str_val = BytesField(0x84)
    tok_val = BytesField(0x85)
    cert = BytesField(0x86)
    chain = BytesField(0x87)
    #tag = BytesField(0x88)
    template = BytesField(0x88)
    publication = BytesField(0x89)

class TrustSchemaModel(TlvModel):
    inner = ModelField(0x83,NestedModel)

class Policy:
    pass

class Identifier:
    def __init__(self):
        self.type = None
        self.value = None
        self.signedby = None
        
class Expression:
    def __init__(self):
        self.type = None
        self.value = None

class CustomVisitor(epVisitor):
    def __init__(self):
        self.statements = []
    
    def visitPolicy(self, ctx:epParser.PolicyContext):
        policy = Policy()
        policy.name = "Policy"
        s = []
        for c in ctx.statement():
            s.append(c.accept(self))
        policy.statement = s
        self.statements.append(policy)
    
    def visitStatement(self, ctx:epParser.StatementContext):
        id = ctx.identifier().accept(self)
        
        if(id.type == 'uString'):
            idDict[id.value] = ctx.expression().accept(self).value
        
        else:
            exp = ctx.expression().accept(self)
            
            granularities = ctx.granularities().accept(self) if ctx.granularities() else None
            constraints = ctx.constraints().accept(self) if ctx.constraints() else None
            
            defDict[id.value].append(exp)
            defDict[id.value].append(granularities)
            defDict[id.value].append(constraints)
            
            
            #if(granularities):
                #for c in granularities:
                    #signer[id.value].append(c.value)
            '''
            if(constraints):
                cons[id.value] = constraints
            
            if(id.type == 'hString'):
                primary.append(id.value)
        
            elif(exp.type == 'id'):
                parent[exp.value.value].append(id.value)
                parentList.add(exp.value.value)
                childList.append(id.value)
                children[id.value] = exp.value.value
            '''
            #if(exp.type == 'id' and exp.value.type == 'hString' and constraints):
                #templateDict[id.value] = [-1,-1]
            
            
    def visitIdentifier(self, ctx:epParser.IdentifierContext):
        id = Identifier()
        
        if(ctx.STRING()):
            id.type = 'string'
            id.value = ctx.STRING().getText()
            
        elif(ctx.ustring()):
            id.type = 'uString'
            id.value = ctx.ustring().accept(self)
        
        elif (ctx.hstring()):
            id.type = 'hString'
            id.value = ctx.hstring().accept(self)
            
        return id
            
    def visitConstraints(self, ctx:epParser.ConstraintsContext):
        cl = []
        for c in ctx.constraint():
            cl.append(c.accept(self))
        return cl
            
    def visitConstraint(self, ctx:epParser.ConstraintContext):
        l = []
        d = {}
        #print(len(ctx.constraint_body()))
        for c in ctx.constraint_body():
            i, s = c.accept(self)
            d[i.value] = s
        return d
        
    def visitConstraint_body(self, ctx:epParser.Constraint_bodyContext):
        id = ctx.identifier().accept(self)
        s = []
        #print(len(ctx.components()))
        for c in ctx.components():
            s.append(c.accept(self))
        '''if(ctx.literal()):
            s = ctx.literal().accept(self)
        elif(ctx.function):
            s = ctx.function().accept(self)+'()'''
        return id, s
    
    def visitComponents(self, ctx:epParser.ComponentsContext):
        if(ctx.literal()):
            s = ctx.literal().accept(self)
        elif(ctx.function):
            s = ctx.function().accept(self)+'()'
        return s
        
    def visitGranularities(self, ctx:epParser.GranularitiesContext):
        grans = []
        for i in ctx.granularity():
            grans.append(i.accept(self))
            #certDict[i.accept(self).value] = [-1,-1]
        return grans
    
    def visitUstring(self, ctx:epParser.UstringContext):
        return ctx.UNDERSCORE().getText() + ctx.STRING().getText()
        
    def visitHstring(self, ctx:epParser.HstringContext):
        return ctx.HASH().getText() + ctx.STRING().getText()
        
    def visitLiteral(self, ctx:epParser.LiteralContext):
        tokenDict[ctx.STRING().getText()] = [-1,-1,-1]
        literalList.append(ctx.STRING().getText())
        return ctx.STRING().getText()
    
    def visitFunction(self, ctx:epParser.FunctionContext):
        return ctx.STRING().getText()
        
    def visitExpression(self, ctx:epParser.ExpressionContext):
        e = Expression()
        if (ctx.name()):
            e.value = ctx.name().accept(self)
            e.type = 'name'
        elif (ctx.identifier()):
            e.value = ctx.identifier().accept(self)
            e.type = 'id'
        elif (ctx.literal()):
            e.value = ctx.literal().accept(self)
            e.type = 'literal'
        return e
    
    def visitName(self, ctx:epParser.NameContext):
        components = []
        for c in ctx.component():
            components.append(c.accept(self))
            tokenDict[c.accept(self).value] = [-1,-1,-1]
        return components

def expand():
    for id,values in defDict.items():
        #print(id,values)
        name = values[0]
        components = []
        if (name.type == 'id'):
            name = defDict[name.value.value][0].value
        else:
            name = name.value

        for n in name:
            if(n.value in idDict):
                components.append(idDict[n.value])
            else:
                components.append(n.value)
        #print(components)
        
        grans = values[1]
        granularities = []
        for gran in grans:
            granularity = []
            if (type(gran.value) == list):
                for g in gran.value:
                    granularity.append(g.value)
            #for g in granularity:
                #print(g.value)
            else:
                granularity.append(gran.value.value)
            granularities.append(granularity)
        #print(granularities)
        
        #print(grans)
        ### NEED TO HANDLE THE CONSTRAINTS PART
        cons = values[2][0]
        lis = list(product(*cons.values()))
        #print(lis)
        
        for l in lis:
            idx = 0
            temDic = {}
            for k,v in cons.items():
                temDic[k] = l[idx]
                idx += 1
            #print(temDic)
            temp = components.copy()
            #print(temp)
            for a,b in temDic.items():
                temp = list(map(lambda x: x.replace(a, b), temp))
            #print(temp)
            
            res = ''
            for t in temp:
                res += '/'+t
            #print(res)
            
            tempGrans = []
            for gran in granularities:
                tempGran = gran.copy()
                for a,b in temDic.items():
                    tempGran = list(map(lambda x: x.replace(a, b), tempGran))
                g = ''
                for t in tempGran:
                    g += '/'+t
                KEKDict[res].append(g)
                
        
        '''for k,v in cons.items():
            print(k,v)
            
            for i in v:
                new = list(map(lambda x: x.replace(k, i), components))
                print(new)'''
                
            
        
        
        
def get_parse_tree(file_name):
    schema_src_code = FileStream(file_name)
    lexer = epLexer(schema_src_code)
    stream = CommonTokenStream(lexer)
    parser = epParser(stream)
    tree = parser.policy()
    return tree, parser.getNumberOfSyntaxErrors()
    
def formatPrint(dic):
    for key,val in dic.items():
        print('{0}  ------->   {1}'.format(key,val))
    print('\n')
    
def listPrint(l):
    for n in l:
        print (n)
    print('\n')

    

tree, err = get_parse_tree(sys.argv[1])
if err == 0:
    visitor = CustomVisitor()
    try:
        tree.accept(visitor)
        #print(idDict)

    except Exception as e:
        print("\nSyntax error occurred in the policy file!\n")
        sys.exit(1)
    #formatPrint(defDict)
    expand()
    formatPrint(KEKDict)

    
    
    
    
        
