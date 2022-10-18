# Generated from dp.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dpParser import dpParser
else:
    from dpParser import dpParser

# This class defines a complete generic visitor for a parse tree produced by dpParser.

class dpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by dpParser#policy.
    def visitPolicy(self, ctx:dpParser.PolicyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#statement.
    def visitStatement(self, ctx:dpParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#rolePolicy.
    def visitRolePolicy(self, ctx:dpParser.RolePolicyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#rulePolicy.
    def visitRulePolicy(self, ctx:dpParser.RulePolicyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#expression.
    def visitExpression(self, ctx:dpParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#encryptor.
    def visitEncryptor(self, ctx:dpParser.EncryptorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#name.
    def visitName(self, ctx:dpParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#component.
    def visitComponent(self, ctx:dpParser.ComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#identifier.
    def visitIdentifier(self, ctx:dpParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#literal.
    def visitLiteral(self, ctx:dpParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#constraints.
    def visitConstraints(self, ctx:dpParser.ConstraintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#constraint.
    def visitConstraint(self, ctx:dpParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#constraint_body.
    def visitConstraint_body(self, ctx:dpParser.Constraint_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#components.
    def visitComponents(self, ctx:dpParser.ComponentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#function.
    def visitFunction(self, ctx:dpParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#granularities.
    def visitGranularities(self, ctx:dpParser.GranularitiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#granularity.
    def visitGranularity(self, ctx:dpParser.GranularityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#ustring.
    def visitUstring(self, ctx:dpParser.UstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#hstring.
    def visitHstring(self, ctx:dpParser.HstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#variable.
    def visitVariable(self, ctx:dpParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by dpParser#slash.
    def visitSlash(self, ctx:dpParser.SlashContext):
        return self.visitChildren(ctx)



del dpParser