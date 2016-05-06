from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from parser.MetrinkLexer import MetrinkLexer
from parser.MetrinkParser import MetrinkParser
from QueryBuilderVisitor import QueryBuilderVisitor


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
            lexer = MetrinkLexer(istream)
            stream = CommonTokenStream(lexer)

            # print out the token parsing
            stream.fill()
            print('INPUT: ' + l)

            for token in stream.tokens:
                if token.text != '<EOF>':
                    print("%s: %s" % (token.text, MetrinkLexer.symbolicNames[token.type-1]))

            parser = MetrinkParser(stream)

            parser.removeErrorListeners()
            parser.addErrorListener(MyErrorListener(l))

            tree = parser.graph_query()


            if tree is not None:
                print('WORKED: ' + l)

            visitor = QueryBuilderVisitor()
            visitor.visit(tree)

            # printer = MetrinkPrintListener()
            # walker = ParseTreeWalker()
            # walker.walk(printer, tree)


