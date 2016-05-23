from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from pandas import DataFrame
from pandas_highcharts.core import serialize

from logger import logger
from parser.MetrinkLexer import MetrinkLexer
from parser.MetrinkParser import MetrinkParser
from QueryBuilderVisitor import QueryBuilderVisitor
from functions.QueryFunction import QueryFunction


class MyErrorListener(ErrorListener):
    def __init__(self, input):
        self.input = input

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("FAILED: %s" % self.input)
        print("%d:%d %s" % (line, column, msg))
        raise ValueError('PARSE FAILED')

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print(str(startIndex) + " to " + str(stopIndex))


def generate_graph(query, chart_div='graph'):
    istream = InputStream(query)
    lexer = MetrinkLexer(istream)
    stream = CommonTokenStream(lexer)

    # fill the token stream
    stream.fill()

    # create a parser
    parser = MetrinkParser(stream)

    # setup a custom error listener
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener(query))

    # construct the AST
    tree = parser.graph_query()

    # walk the AST to get our start, end, and expression
    visitor = QueryBuilderVisitor()
    (start, end, expression) = visitor.visit(tree)

    # run the first function and get the DataFrame
    last_frame = expression[0].process(start, end, DataFrame())

    # go through all the other functions
    for i in range(1, len(expression), 2):
        conn = expression[i]
        fun = expression[i + 1]

        if not isinstance(fun, QueryFunction):
            raise ValueError('NON-QUERY FUNCTION: ' + str(fun))

        cur_frame = fun.process(start, end, last_frame)

        if conn == '>|':  # combine the two
            last_frame = last_frame.combine_first(cur_frame)
        else:
            last_frame = cur_frame

        i += 2

    # fill in any missing data
    last_frame = last_frame.fillna(method='ffill')

    # resample based upon the time
    graph_range = end - start

    if graph_range.days > 1:
        last_frame = last_frame.resample('60T').mean()  # resample to every 60 minutes
    elif graph_range.seconds > 5400:
        last_frame = last_frame.resample('5T').mean()  # if more than 1.5 hours, resample to every 5 minutes

    (rows, cols) = last_frame.shape

    logger.debug('Data Frame size: %d x %d' % (rows, cols))

    # return the chart for rendering with HighCharts
    return serialize(last_frame, render_to=chart_div, output_type='json')
