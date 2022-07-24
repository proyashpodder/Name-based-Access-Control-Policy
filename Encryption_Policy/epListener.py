# Generated from ep.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .epParser import epParser
else:
    from epParser import epParser

# This class defines a complete listener for a parse tree produced by epParser.
class epListener(ParseTreeListener):

    # Enter a parse tree produced by epParser#policy.
    def enterPolicy(self, ctx:epParser.PolicyContext):
        pass

    # Exit a parse tree produced by epParser#policy.
    def exitPolicy(self, ctx:epParser.PolicyContext):
        pass


    # Enter a parse tree produced by epParser#statement.
    def enterStatement(self, ctx:epParser.StatementContext):
        pass

    # Exit a parse tree produced by epParser#statement.
    def exitStatement(self, ctx:epParser.StatementContext):
        pass


    # Enter a parse tree produced by epParser#expression.
    def enterExpression(self, ctx:epParser.ExpressionContext):
        pass

    # Exit a parse tree produced by epParser#expression.
    def exitExpression(self, ctx:epParser.ExpressionContext):
        pass


    # Enter a parse tree produced by epParser#name.
    def enterName(self, ctx:epParser.NameContext):
        pass

    # Exit a parse tree produced by epParser#name.
    def exitName(self, ctx:epParser.NameContext):
        pass


    # Enter a parse tree produced by epParser#component.
    def enterComponent(self, ctx:epParser.ComponentContext):
        pass

    # Exit a parse tree produced by epParser#component.
    def exitComponent(self, ctx:epParser.ComponentContext):
        pass


    # Enter a parse tree produced by epParser#identifier.
    def enterIdentifier(self, ctx:epParser.IdentifierContext):
        pass

    # Exit a parse tree produced by epParser#identifier.
    def exitIdentifier(self, ctx:epParser.IdentifierContext):
        pass


    # Enter a parse tree produced by epParser#literal.
    def enterLiteral(self, ctx:epParser.LiteralContext):
        pass

    # Exit a parse tree produced by epParser#literal.
    def exitLiteral(self, ctx:epParser.LiteralContext):
        pass


    # Enter a parse tree produced by epParser#constraints.
    def enterConstraints(self, ctx:epParser.ConstraintsContext):
        pass

    # Exit a parse tree produced by epParser#constraints.
    def exitConstraints(self, ctx:epParser.ConstraintsContext):
        pass


    # Enter a parse tree produced by epParser#constraint.
    def enterConstraint(self, ctx:epParser.ConstraintContext):
        pass

    # Exit a parse tree produced by epParser#constraint.
    def exitConstraint(self, ctx:epParser.ConstraintContext):
        pass


    # Enter a parse tree produced by epParser#constraint_body.
    def enterConstraint_body(self, ctx:epParser.Constraint_bodyContext):
        pass

    # Exit a parse tree produced by epParser#constraint_body.
    def exitConstraint_body(self, ctx:epParser.Constraint_bodyContext):
        pass


    # Enter a parse tree produced by epParser#components.
    def enterComponents(self, ctx:epParser.ComponentsContext):
        pass

    # Exit a parse tree produced by epParser#components.
    def exitComponents(self, ctx:epParser.ComponentsContext):
        pass


    # Enter a parse tree produced by epParser#function.
    def enterFunction(self, ctx:epParser.FunctionContext):
        pass

    # Exit a parse tree produced by epParser#function.
    def exitFunction(self, ctx:epParser.FunctionContext):
        pass


    # Enter a parse tree produced by epParser#granularities.
    def enterGranularities(self, ctx:epParser.GranularitiesContext):
        pass

    # Exit a parse tree produced by epParser#granularities.
    def exitGranularities(self, ctx:epParser.GranularitiesContext):
        pass


    # Enter a parse tree produced by epParser#granularity.
    def enterGranularity(self, ctx:epParser.GranularityContext):
        pass

    # Exit a parse tree produced by epParser#granularity.
    def exitGranularity(self, ctx:epParser.GranularityContext):
        pass


    # Enter a parse tree produced by epParser#ustring.
    def enterUstring(self, ctx:epParser.UstringContext):
        pass

    # Exit a parse tree produced by epParser#ustring.
    def exitUstring(self, ctx:epParser.UstringContext):
        pass


    # Enter a parse tree produced by epParser#hstring.
    def enterHstring(self, ctx:epParser.HstringContext):
        pass

    # Exit a parse tree produced by epParser#hstring.
    def exitHstring(self, ctx:epParser.HstringContext):
        pass


    # Enter a parse tree produced by epParser#slash.
    def enterSlash(self, ctx:epParser.SlashContext):
        pass

    # Exit a parse tree produced by epParser#slash.
    def exitSlash(self, ctx:epParser.SlashContext):
        pass



del epParser