from antlr4 import *

from gen.metrinkLexer import metrinkLexer
from gen.metrinkListener import metrinkListener
from gen.metrinkParser import metrinkParser


class MetrinkPrintListener(metrinkListener):
    def enterGraph_query(self, ctx:metrinkParser.Graph_queryContext):
        print("%s" % ctx.absolute_date_literal())
        print("%s" % ctx.relative_time_literal())

if __name__ == '__main__':
    test = "2015-01-01 1:1pm metric('blah', 'blah', 'blah')"
    istream = InputStream(test)
    lexer = metrinkLexer(istream)
    stream = CommonTokenStream(lexer)
    parser = metrinkParser(stream)

    print(test)
    tree = parser.graph_query()

    printer = MetrinkPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


