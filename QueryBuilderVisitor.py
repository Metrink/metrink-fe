from parser.MetrinkVisitor import MetrinkVisitor
from parser.MetrinkParser import MetrinkParser

from functions import QUERY_FUNCTIONS
from functions.MathFunction import MathFunction
from functions.MetricFunction import MetricFunction
from functions.LogFunction import LogFunction
from functions.EventFunction import EventFunction

from dateutil import parser
import datetime


class QueryBuilderVisitor(MetrinkVisitor):
    # Visit a parse tree produced by MetrinkParser#metrink_query.
    def visitMetrink_query(self, ctx:MetrinkParser.Metrink_queryContext):
        start_time = self.visit(ctx.children[0])
        end_time = datetime.datetime.now()

        # convert relative to absolute
        if isinstance(start_time, datetime.timedelta):
            start_time = datetime.datetime.now() + start_time

            if start_time > datetime.datetime.now():
                start_time += datetime.timedelta(days=1)

        # check for an end date/time
        if len(ctx.children) == 4:
            end_time = self.visit(ctx.children[2]) # skip the 'to' token

            if end_time > datetime.datetime.now():
                end_time += datetime.timedelta(days=1)

            expression = self.visit(ctx.children[3])
        else:
            expression = self.visit(ctx.children[1])

        if start_time > end_time:
            raise ValueError('Start time must be before end time: ' + str(start_time) + ' > ' + str(end_time))

        return (start_time, end_time, expression)

    # Visit a parse tree produced by MetrinkParser#log_expression.
    def visitLog_expression(self, ctx:MetrinkParser.Log_expressionContext):
        return self.__visit_expression(ctx.children)

    # Visit a parse tree produced by MetrinkParser#event_expression.
    def visitEvent_expression(self, ctx:MetrinkParser.Event_expressionContext):
        return self.__visit_expression(ctx.children)

    # Visit a parse tree produced by MetrinkParser#graph_expression.
    def visitGraph_expression(self, ctx:MetrinkParser.Graph_expressionContext):
        return self.__visit_expression(ctx.children)

    def __visit_expression(self, children):
        flattened_children = []

        # visit all the children, and flatten everything out
        for child in children:
            r = self.visit(child)
            if isinstance(r, list):
                flattened_children.extend(r)
            else:
                flattened_children.append(r)

        c_len = len(flattened_children)
        ret = []

        i = 0
        while i < c_len:
            child = flattened_children[i]
            ret.append(child)

            if i < c_len-1:
                next_child = flattened_children[i+1]

                # add in the implicit copy connector if it's not there
                if not isinstance(next_child, str):
                    ret.append('>|')
                else:
                    ret.append(next_child)
                    i += 1

            i += 1

        return ret

    # Visit a parse tree produced by MetrinkParser#metric.
    def visitMetric(self, ctx: MetrinkParser.MetricContext):
        field_lists = self._collect_fields(ctx.children)
        overlay = None

        # check to see if we have a time overlay
        if len(field_lists) != len(ctx.children)-3:
            overlay = self.visit(ctx.children[-2])

        return MetricFunction(field_lists, overlay)

    # Visit a parse tree produced by MetrinkParser#log.
    def visitLog(self, ctx:MetrinkParser.LogContext):
        field_lists = self._collect_fields(ctx.children)

        if 'index' not in field_lists:
            raise ValueError('Log must include a field named index')

        return LogFunction(field_lists['index'], field_lists)

    # Visit a parse tree produced by MetrinkParser#event.
    def visitEvent(self, ctx:MetrinkParser.EventContext):
        field_lists = self._collect_fields(ctx.children)

        return EventFunction(field_lists)

    def _collect_fields(self, children):
        field_lists = dict()

        for child in children[2:]:
            res = self.visit(child)

            if isinstance(res, list) and len(res) == 2:
                if res[0] in field_lists:  # cannot have duplicate field names; messes up metric parsing above
                    raise ValueError('Duplicate field found: ' + str(res[0]))

                field_lists[res[0]] = res[1]

        return field_lists


    # Visit a parse tree produced by MetrinkParser#field_list.
    def visitField_list(self, ctx:MetrinkParser.Field_listContext):
        field = self.visit(ctx.children[0])
        field_values = self.visit(ctx.children[2])

        # always force it into a list
        field_values = [field_values] if not isinstance(field_values, list) else field_values

        return field, field_values

    # Visit a parse tree produced by MetrinkParser#connector.
    def visitConnector(self, ctx: MetrinkParser.ConnectorContext):
        return self.visitChildren(ctx) # this just grabs the character

    # Visit a parse tree produced by MetrinkParser#string_array.
    def visitString_array(self, ctx: MetrinkParser.String_arrayContext):
        ret = []

        for child in ctx.children[1:-1]:
            ret.append(self.visit(child))

        # filter out all the commas
        return [r for r in ret if r != ',']

    # Visit a parse tree produced by MetrinkParser#function.
    def visitFunction(self, ctx: MetrinkParser.FunctionContext):
        name = self.visit(ctx.children[0])

        if name not in QUERY_FUNCTIONS.keys():
            raise ValueError("Unknown function: " + str(name))

        # check for arguments
        if len(ctx.children) != 1:
            args = [a for a in self.visit(ctx.children[1])[1:-1] if a != ',']
        else:
            args = []

        # need to make sure we only have single arguments for functions
        for i in range(0, len(args)):
            if isinstance(args[i], list):
                if len(args[i]) > 1:
                    raise ValueError("Array arguments not supported")
                else:
                    args[i] = args[i][0]

        return QUERY_FUNCTIONS[name](name, args)

    # Visit a parse tree produced by MetrinkParser#argument_list.
    def visitArgument_list(self, ctx: MetrinkParser.Argument_listContext):
        ret = []

        for child in ctx.children:
            ret.append(self.visit(child))

        # filter out all the commas
        return [r for r in ret if r != ',']

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

        if op not in ('+', '-', '*', '/'):
            raise ValueError("Unknown operator: " + op)

        if (isinstance(left_child, list) and len(left_child) > 1) or\
           (isinstance(right_child, list) and len(right_child) > 1):
            raise ValueError("Invalid arguments to " + str(op))

        left_child = left_child[0] if isinstance(left_child, list) else left_child
        right_child = right_child[0] if isinstance(right_child, list) else right_child

        if isinstance(left_child, list) or isinstance(right_child, list):
            print("HERE")

        return MathFunction(op, (left_child, right_child))

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

        # filter out all the commas
        return [r for r in ret if r != ',']

    # Visit a parse tree produced by MetrinkParser#relative_time_literal.
    def visitRelative_time_literal(self, ctx: MetrinkParser.Relative_time_literalContext):
        num = int(ctx.children[0].getText())

        # convert everything into seconds
        if ctx.children[1].getText() == 's':
            delta = datetime.timedelta(seconds=num)
        elif ctx.children[1].getText() == 'm':
            delta = datetime.timedelta(minutes=num)
        elif ctx.children[1].getText() == 'h':
            delta = datetime.timedelta(hours=num)
        elif ctx.children[1].getText() == 'd':
            delta = datetime.timedelta(days=num)
        else:
            raise ValueError("Unknown time: %s" % ctx.children[1].getText())

        return delta

    # Visit a parse tree produced by MetrinkParser#absolute_date_time_literal.
    def visitAbsolute_date_time_literal(self, ctx:MetrinkParser.Absolute_date_time_literalContext):
        date = self.visit(ctx.children[0])
        time = self.visit(ctx.children[1])

        return datetime.datetime(year=date.year, month=date.month, day=date.day, hour=time.hour, minute=time.minute)

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

        # Visit a parse tree produced by MetrinkParser#regex_literal.
    def visitRegex_literal(self, ctx: MetrinkParser.Regex_literalContext):
        self.visitChildren(ctx)

        regex_lit = ctx.getText()[1:-1]  # chop off the brances

    # Visit a parse tree produced by MetrinkParser#string_literal.
    def visitString_literal(self, ctx: MetrinkParser.String_literalContext):
        self.visitChildren(ctx)

        str_lit = ctx.getText()[1:-1]  # chop off the quotes

        return str_lit

    def visitTerminal(self, node):
        return str(node)