from antlr4 import *
from dpLexer import dpLexer
from dpListener import dpListener
from dpParser import dpParser
from dpVisitor import dpVisitor
import sys
import binascii
from collections import defaultdict
from ndn.encoding import *
from itertools import product

idDict = {}
defDict = defaultdict(list)
expandDict = defaultdict(list)
tempDict = {}
tempRoleDict = defaultdict(list)
tempRuleDict = defaultdict(list)
#tempRoleDict[1].append = 2
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

class CustomVisitor(dpVisitor):
    def __init__(self):
        self.statements = []
    
    def visitPolicy(self, ctx:dpParser.PolicyContext):
        policy = Policy()
        policy.name = "Policy"
        s = []
        for c in ctx.statement():
            s.append(c.accept(self))
        policy.statement = s
        self.statements.append(policy)
        
        
    def visitRolePolicy(self, ctx:dpParser.RolePolicyContext):
        id = ctx.identifier().accept(self)
        if(id.type == 'uString'):
            idDict[id.value] = ctx.expression().accept(self).value
        else:
            exp = ctx.expression().accept(self)
            constraints = ctx.constraints().accept(self) if ctx.constraints() else None
            #encryptor = ctx.encryptor().accept(self) if ctx.encryptor() else None

            tempRoleDict[id.value].append(exp)
            tempRoleDict[id.value].append(constraints)
            #tempRoleDict[id.value].append(encryptor)
    def visitRulePolicy(self, ctx:dpParser.RulePolicyContext):
        id = ctx.identifier().accept(self)
        if(id.type == 'uString'):
            idDict[id.value] = ctx.expression().accept(self).value
        else:
            grans = ctx.granularities().accept(self)
            #constraints = ctx.constraints().accept(self) if ctx.constraints() else None
            encryptor = ctx.encryptor().accept(self) if ctx.encryptor() else None

            tempRuleDict[id.value].append(grans)
            #tempRoleDict[id.value].append(constraints)
            tempRuleDict[id.value].append(encryptor)
            
    def visitIdentifier(self, ctx:dpParser.IdentifierContext):
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
            
        elif (ctx.variable()):
            id.type = 'variable'
            id.value = ctx.variable().accept(self)
            
        return id
        
    def visitEncryptor(self, ctx:dpParser.EncryptorContext):
        en = []
        for e in ctx.identifier():
            en.append(e)
        return en
            
    def visitConstraints(self, ctx:dpParser.ConstraintsContext):
        cl = []
        for c in ctx.constraint():
            cl.append(c.accept(self))
        return cl
            
    def visitConstraint(self, ctx:dpParser.ConstraintContext):
        l = []
        d = {}
        #print(len(ctx.constraint_body()))
        for c in ctx.constraint_body():
            i, s = c.accept(self)
            d[i.value] = s
        return d
        
    def visitConstraint_body(self, ctx:dpParser.Constraint_bodyContext):
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
    
    def visitComponents(self, ctx:dpParser.ComponentsContext):
        if(ctx.literal()):
            s = ctx.literal().accept(self)
        elif(ctx.function):
            s = ctx.function().accept(self)+'()'
        return s
        
    def visitGranularities(self, ctx:dpParser.GranularitiesContext):
        grans = []
        for i in ctx.granularity():
            grans.append(i.accept(self))
            #certDict[i.accept(self).value] = [-1,-1]
        return grans
    
    def visitGranularity(self, ctx:dpParser.GranularityContext):
        exp = ctx.expression().accept(self)
        constraints = ctx.constraints().accept(self) if ctx.constraints() else None
        
        return (exp,constraints)
        
        
    def visitUstring(self, ctx:dpParser.UstringContext):
        return ctx.UNDERSCORE().getText() + ctx.STRING().getText()
        
    def visitHstring(self, ctx:dpParser.HstringContext):
        return ctx.HASH().getText() + ctx.STRING().getText()
    
    def visitVariable(self, ctx:dpParser.VariableContext):
        return ctx.STRING().getText()
        
    def visitLiteral(self, ctx:dpParser.LiteralContext):
        tokenDict[ctx.STRING().getText()] = [-1,-1,-1]
        literalList.append(ctx.STRING().getText())
        return ctx.STRING().getText()
    
    def visitFunction(self, ctx:dpParser.FunctionContext):
        return ctx.STRING().getText()
        
    def visitExpression(self, ctx:dpParser.ExpressionContext):
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
    
    def visitName(self, ctx:dpParser.NameContext):
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
            elif(n.type == 'variable'):
                components.append(n.value)
            else:
                components.append('_')
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
                    if(t in idDict):
                        g+= '/'+idDict[t]
                    else:
                        g += '/'+t
                tempGrans.append(g)
            KEKDict[res] = tempGrans
                
            
        
        
        
def get_parse_tree(file_name):
    schema_src_code = FileStream(file_name)
    lexer = dpLexer(schema_src_code)
    stream = CommonTokenStream(lexer)
    parser = dpParser(stream)
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
        print(idDict)

    except Exception as e:
        print("\nSyntax error occurred in the policy file!\n")
        sys.exit(1)
    formatPrint(tempRoleDict)
    formatPrint(tempRuleDict)
    #expand()
    #formatPrint(KEKDict)

    
    
    
    
        
