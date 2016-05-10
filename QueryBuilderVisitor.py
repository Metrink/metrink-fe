from parser.MetrinkVisitor import MetrinkVisitor
from parser.MetrinkParser import MetrinkParser
from functions.MathFunction import MathFunction
from functions.MetricFunction import MetricFunction

from dateutil import parser
import datetime

class QueryBuilderVisitor(MetrinkVisitor):
    # Visit a parse tree produced by MetrinkParser#graph_query.
    def visitGraph_query(self, ctx: MetrinkParser.Graph_queryContext):
        ret = self.visitChildren(ctx)

        return ret


    # Visit a parse tree produced by MetrinkParser#graph_expression.
    def visitGraph_expression(self, ctx: MetrinkParser.Graph_expressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MetrinkParser#connector.
    def visitConnector(self, ctx: MetrinkParser.ConnectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MetrinkParser#metric.
    def visitMetric(self, ctx: MetrinkParser.MetricContext):
        # 8 or 10 children depending upon if we have a time layover
        # don't care about the first two
        host = self.visit(ctx.children[2])
        group = self.visit(ctx.children[4])
        name = self.visit(ctx.children[6])

        # convert everything to an array
        hosts = host if isinstance(host, list) else (host, )
        groups = group if isinstance(group, list) else (group, )
        names = name if isinstance(name, list) else (name, )

        if len(ctx.children) == 10:
            raise NotImplementedError('Time overlays are not yet implemented')

        ret = []

        for host in hosts:
            for group in groups:
                for name in names:
                    ret.append(MetricFunction(host, group, name))

        return ret

    # Visit a parse tree produced by MetrinkParser#string_array.
    def visitString_array(self, ctx: MetrinkParser.String_arrayContext):
        ret = []

        for child in ctx.children:
            ret.append(self.visit(child))

        return ret


    # Visit a parse tree produced by MetrinkParser#function.
    def visitFunction(self, ctx: MetrinkParser.FunctionContext):
        return ctx.getText()


    # Visit a parse tree produced by MetrinkParser#argument_list.
    def visitArgument_list(self, ctx: MetrinkParser.Argument_listContext):
        ret = []

        for child in ctx.children:
            ret.append(self.visit(child))

        return ret


    # Visit a parse tree produced by MetrinkParser#argument.
    def visitArgument(self, ctx: MetrinkParser.ArgumentContext):
        if len(ctx.children) != 1:
            raise ValueError("Having to parse more than one argument")

        return self.visit(ctx.children[0])


    # Visit a parse tree produced by MetrinkParser#additive_expression.
    def visitAdditive_expression(self, ctx: MetrinkParser.Additive_expressionContext):
        return self._handle_math_function(ctx)


    # Visit a parse tree produced by MetrinkParser#multiplicative_expression.
    def visitMultiplicative_expression(self, ctx: MetrinkParser.Multiplicative_expressionContext):
        return self._handle_math_function(ctx)

    def _handle_math_function(self, ctx):
        left_child = self.visit(ctx.children[0])

        # if we only have 1 child, keep going
        if len(ctx.children) == 1:
            return left_child


        op = self.visit(ctx.children[1])
        right_child = self.visit(ctx.children[2])

        if op == '+':
            return MathFunction(MathFunction.ADD, left_child, right_child)
        elif op == '-':
            return MathFunction(MathFunction.SUB, left_child, right_child)
        elif op == '*':
            return MathFunction(MathFunction.MUL, left_child, right_child)
        elif op == '/':
            return MathFunction(MathFunction.DIV, left_child, right_child)
        else:
            raise ValueError("Unknown math fucntion: " + str(op))

    # Visit a parse tree produced by MetrinkParser#number_literal.
    def visitNumber_literal(self, ctx: MetrinkParser.Number_literalContext):
        self.visitChildren(ctx)

        num = ctx.getText()

        if '.' in num:
            return float(num)
        else:
            return int(num)


    # Visit a parse tree produced by MetrinkParser#relative_time_array.
    def visitRelative_time_array(self, ctx: MetrinkParser.Relative_time_arrayContext):
        ret = []

        for child in ctx.children:
            ret.append(self.visit(child))

        return ret


    # Visit a parse tree produced by MetrinkParser#relative_time_literal.
    def visitRelative_time_literal(self, ctx: MetrinkParser.Relative_time_literalContext):
        num = int(ctx.children[0].getText())

        if num > 0:
            raise ValueError("Relative times must be negative")

        num *= -1

        # convert everything into seconds
        if ctx.children[1].getText() == 's':
            delta = datetime.timedelta(seconds=num)
        elif ctx.children[1].getText() == 'm':
            delta = datetime.timedelta(minutes=num)
        elif ctx.children[1].getText() == 'h':
            delta = datetime.timedelta(hours=num)
        elif ctx.children[1].getText() == 'd':
            delta = datetime.timedelta(days=num)

        return datetime.datetime.now() - delta


    # Visit a parse tree produced by MetrinkParser#absolute_date_literal.
    def visitAbsolute_date_literal(self, ctx: MetrinkParser.Absolute_date_literalContext):
        self.visitChildren(ctx)

        return parser.parse(ctx.getText())


    # Visit a parse tree produced by MetrinkParser#absolute_time_literal.
    def visitAbsolute_time_literal(self, ctx: MetrinkParser.Absolute_time_literalContext):
        self.visitChildren(ctx)

        return parser.parse(ctx.getText())


    # Visit a parse tree produced by MetrinkParser#percent_literal.
    def visitPercent_literal(self, ctx: MetrinkParser.Percent_literalContext):
        raise NotImplementedError("Percent Literal not yet implemented")
        # return self.visitChildren(ctx)


    # Visit a parse tree produced by MetrinkParser#boolean_literal.
    def visitBoolean_literal(self, ctx: MetrinkParser.Boolean_literalContext):
        self.visitChildren(ctx)

        if 'true' == ctx.getText().lower():
            return True
        else:
            return False


    # Visit a parse tree produced by MetrinkParser#string_literal.
    def visitString_literal(self, ctx: MetrinkParser.String_literalContext):
        self.visitChildren(ctx)

        str_lit = ctx.getText()[1:-1] # chop off the quotes

        return str_lit

    def visitTerminal(self, node):
        return str(node)