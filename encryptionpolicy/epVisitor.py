# Generated from ep.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .epParser import epParser
else:
    from epParser import epParser

# This class defines a complete generic visitor for a parse tree produced by epParser.

class epVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by epParser#policy.
    def visitPolicy(self, ctx:epParser.PolicyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#statement.
    def visitStatement(self, ctx:epParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#expression.
    def visitExpression(self, ctx:epParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#name.
    def visitName(self, ctx:epParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#component.
    def visitComponent(self, ctx:epParser.ComponentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#identifier.
    def visitIdentifier(self, ctx:epParser.IdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#literal.
    def visitLiteral(self, ctx:epParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#constraints.
    def visitConstraints(self, ctx:epParser.ConstraintsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#constraint.
    def visitConstraint(self, ctx:epParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#constraint_body.
    def visitConstraint_body(self, ctx:epParser.Constraint_bodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#components.
    def visitComponents(self, ctx:epParser.ComponentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#function.
    def visitFunction(self, ctx:epParser.FunctionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#granularities.
    def visitGranularities(self, ctx:epParser.GranularitiesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#granularity.
    def visitGranularity(self, ctx:epParser.GranularityContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#ustring.
    def visitUstring(self, ctx:epParser.UstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#hstring.
    def visitHstring(self, ctx:epParser.HstringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#variable.
    def visitVariable(self, ctx:epParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by epParser#slash.
    def visitSlash(self, ctx:epParser.SlashContext):
        return self.visitChildren(ctx)



del epParser