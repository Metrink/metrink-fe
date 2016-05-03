from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from gen.metrinkLexer import metrinkLexer
from gen.metrinkListener import metrinkListener
from gen.metrinkParser import metrinkParser

import sys


class MetrinkPrintListener(metrinkListener):
    def enterGraph_query(self, ctx:metrinkParser.Graph_queryContext):
        print("%s" % ctx.absolute_date_literal())
        print("%s" % ctx.relative_time_literal())


class MyErrorListener(ErrorListener):
    def __init__(self, input):
        self.input = input

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("FAILED: %s" % self.input)
        print("%d:%d %s" % (line, column, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print(str(startIndex) + " to " + str(stopIndex))


if __name__ == '__main__':
    with open('valid_queries.txt', 'r') as f:
        for l in f:
            l = l.rstrip()
            if len(l) < 2:
                continue

            istream = InputStream(l)
            lexer = metrinkLexer(istream)
            stream = CommonTokenStream(lexer)
            parser = metrinkParser(stream)

            parser.removeErrorListeners()
            parser.addErrorListener(MyErrorListener(l))

            tree = parser.graph_query()


            if tree is not None:
                print('WORKED: ' + l)

            # printer = MetrinkPrintListener()
            # walker = ParseTreeWalker()
            # walker.walk(printer, tree)


