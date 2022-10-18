# Generated from dp.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .dpParser import dpParser
else:
    from dpParser import dpParser

# This class defines a complete listener for a parse tree produced by dpParser.
class dpListener(ParseTreeListener):

    # Enter a parse tree produced by dpParser#policy.
    def enterPolicy(self, ctx:dpParser.PolicyContext):
        pass

    # Exit a parse tree produced by dpParser#policy.
    def exitPolicy(self, ctx:dpParser.PolicyContext):
        pass


    # Enter a parse tree produced by dpParser#statement.
    def enterStatement(self, ctx:dpParser.StatementContext):
        pass

    # Exit a parse tree produced by dpParser#statement.
    def exitStatement(self, ctx:dpParser.StatementContext):
        pass


    # Enter a parse tree produced by dpParser#rolePolicy.
    def enterRolePolicy(self, ctx:dpParser.RolePolicyContext):
        pass

    # Exit a parse tree produced by dpParser#rolePolicy.
    def exitRolePolicy(self, ctx:dpParser.RolePolicyContext):
        pass


    # Enter a parse tree produced by dpParser#rulePolicy.
    def enterRulePolicy(self, ctx:dpParser.RulePolicyContext):
        pass

    # Exit a parse tree produced by dpParser#rulePolicy.
    def exitRulePolicy(self, ctx:dpParser.RulePolicyContext):
        pass


    # Enter a parse tree produced by dpParser#expression.
    def enterExpression(self, ctx:dpParser.ExpressionContext):
        pass

    # Exit a parse tree produced by dpParser#expression.
    def exitExpression(self, ctx:dpParser.ExpressionContext):
        pass


    # Enter a parse tree produced by dpParser#encryptor.
    def enterEncryptor(self, ctx:dpParser.EncryptorContext):
        pass

    # Exit a parse tree produced by dpParser#encryptor.
    def exitEncryptor(self, ctx:dpParser.EncryptorContext):
        pass


    # Enter a parse tree produced by dpParser#name.
    def enterName(self, ctx:dpParser.NameContext):
        pass

    # Exit a parse tree produced by dpParser#name.
    def exitName(self, ctx:dpParser.NameContext):
        pass


    # Enter a parse tree produced by dpParser#component.
    def enterComponent(self, ctx:dpParser.ComponentContext):
        pass

    # Exit a parse tree produced by dpParser#component.
    def exitComponent(self, ctx:dpParser.ComponentContext):
        pass


    # Enter a parse tree produced by dpParser#identifier.
    def enterIdentifier(self, ctx:dpParser.IdentifierContext):
        pass

    # Exit a parse tree produced by dpParser#identifier.
    def exitIdentifier(self, ctx:dpParser.IdentifierContext):
        pass


    # Enter a parse tree produced by dpParser#literal.
    def enterLiteral(self, ctx:dpParser.LiteralContext):
        pass

    # Exit a parse tree produced by dpParser#literal.
    def exitLiteral(self, ctx:dpParser.LiteralContext):
        pass


    # Enter a parse tree produced by dpParser#constraints.
    def enterConstraints(self, ctx:dpParser.ConstraintsContext):
        pass

    # Exit a parse tree produced by dpParser#constraints.
    def exitConstraints(self, ctx:dpParser.ConstraintsContext):
        pass


    # Enter a parse tree produced by dpParser#constraint.
    def enterConstraint(self, ctx:dpParser.ConstraintContext):
        pass

    # Exit a parse tree produced by dpParser#constraint.
    def exitConstraint(self, ctx:dpParser.ConstraintContext):
        pass


    # Enter a parse tree produced by dpParser#constraint_body.
    def enterConstraint_body(self, ctx:dpParser.Constraint_bodyContext):
        pass

    # Exit a parse tree produced by dpParser#constraint_body.
    def exitConstraint_body(self, ctx:dpParser.Constraint_bodyContext):
        pass


    # Enter a parse tree produced by dpParser#components.
    def enterComponents(self, ctx:dpParser.ComponentsContext):
        pass

    # Exit a parse tree produced by dpParser#components.
    def exitComponents(self, ctx:dpParser.ComponentsContext):
        pass


    # Enter a parse tree produced by dpParser#function.
    def enterFunction(self, ctx:dpParser.FunctionContext):
        pass

    # Exit a parse tree produced by dpParser#function.
    def exitFunction(self, ctx:dpParser.FunctionContext):
        pass


    # Enter a parse tree produced by dpParser#granularities.
    def enterGranularities(self, ctx:dpParser.GranularitiesContext):
        pass

    # Exit a parse tree produced by dpParser#granularities.
    def exitGranularities(self, ctx:dpParser.GranularitiesContext):
        pass


    # Enter a parse tree produced by dpParser#granularity.
    def enterGranularity(self, ctx:dpParser.GranularityContext):
        pass

    # Exit a parse tree produced by dpParser#granularity.
    def exitGranularity(self, ctx:dpParser.GranularityContext):
        pass


    # Enter a parse tree produced by dpParser#ustring.
    def enterUstring(self, ctx:dpParser.UstringContext):
        pass

    # Exit a parse tree produced by dpParser#ustring.
    def exitUstring(self, ctx:dpParser.UstringContext):
        pass


    # Enter a parse tree produced by dpParser#hstring.
    def enterHstring(self, ctx:dpParser.HstringContext):
        pass

    # Exit a parse tree produced by dpParser#hstring.
    def exitHstring(self, ctx:dpParser.HstringContext):
        pass


    # Enter a parse tree produced by dpParser#variable.
    def enterVariable(self, ctx:dpParser.VariableContext):
        pass

    # Exit a parse tree produced by dpParser#variable.
    def exitVariable(self, ctx:dpParser.VariableContext):
        pass


    # Enter a parse tree produced by dpParser#slash.
    def enterSlash(self, ctx:dpParser.SlashContext):
        pass

    # Exit a parse tree produced by dpParser#slash.
    def exitSlash(self, ctx:dpParser.SlashContext):
        pass



del dpParser