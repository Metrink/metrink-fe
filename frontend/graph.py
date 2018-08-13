from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from pandas import DataFrame
from pandas_highcharts.core import serialize

from logger import logger
from QueryBuilderVisitor import QueryBuilderVisitor
from functions.QueryFunction import QueryFunction
from parser.MetrinkFrontendLexer import MetrinkFrontendLexer
from parser.MetrinkFrontendParser import MetrinkFrontendParser


class MyErrorListener(ErrorListener):
    def __init__(self, input):
        self.input = input

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("FAILED: %s" % self.input)
        print("%d:%d %s" % (line, column, msg))
        raise ValueError('PARSE FAILED')

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print(str(startIndex) + " to " + str(stopIndex))


def parse_query(query:str) -> (str,str,list,DataFrame):
    """
    Processes a query and returns the start, end, and QueryFunction
    :param query: the string to parse as a query
    :return: the start, end, expression, and QueryFunction
    """
    istream = InputStream(query)
    lexer = MetrinkFrontendLexer(istream)
    stream = CommonTokenStream(lexer)

    # fill the token stream
    stream.fill()

    for token in stream.tokens:
        if token.text != '<EOF>':
            print("%s: %s" % (token.text, MetrinkFrontendLexer.symbolicNames[token.type-1]))


    # create a parser
    parser = MetrinkFrontendParser(stream)

    # setup a custom error listener
    parser.removeErrorListeners()
    parser.addErrorListener(MyErrorListener(query))

    # construct the AST
    tree = parser.metrink_query()

    # walk the AST to get our start, end, and expression
    visitor = QueryBuilderVisitor()

    start, end, expressions = visitor.visit(tree)

    # run the first function and get the DataFrame
    last_frame = expressions[0].process(start, end, DataFrame())

    # go through all the other functions
    for i in range(1, len(expressions), 2):
        conn = expressions[i]
        fun = expressions[i + 1]

        if not isinstance(fun, QueryFunction):
            raise ValueError('NON-QUERY FUNCTION: ' + str(fun))

        cur_frame = fun.process(start, end, last_frame)

        if conn == '>|':  # combine the two
            last_frame = last_frame.combine_first(cur_frame)
        else:
            last_frame = cur_frame

        logger.debug("FRAME: %d" % i)
        logger.debug("\n" + str(last_frame.head()))

        i += 2

    return start, end, expressions, last_frame


def generate_table(start, end, data_frame, table_div='table'):
    data_set = 'var dataSet = [\n'

    for row in data_frame.iterrows():
        data_set += '[' + ',\n'.join(map(lambda c: '"' + c.replace('"', '\\"').replace('/', '\/') + '"', row[1].values)) + '],\n'

    data_set += '];'

    columns = '[' + ',\n'.join(map(lambda h: '{ title: "' + h.replace('"', '\\"').replace('/', '\/') + '"}', data_frame.columns.values)) + ']'

    function = """
        $(document).ready(function() {
            $('#%s').DataTable({
                data: dataSet,
                columns: %s
            });
        });""" % (table_div, columns)

    return data_set + '\n\n' + function


def generate_graph(title, start, end, data_frame, chart_div='graph'):
    # resample to fill in anything that might be missing
    data_frame = Zabbix.resample_metrics(data_frame, start, end)

    print(data_frame.head())

    # (rows, cols) = last_frame.shape
    # logger.debug('Data Frame size: %d x %d' % (rows, cols))

    # return the chart for rendering with HighCharts
    return serialize(data_frame, render_to=chart_div, output_type='json', title=title)
