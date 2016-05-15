from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from pandas import DataFrame
from sys import stdin

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
            print()
            print('INPUT: ' + l)

            # for token in stream.tokens:
            #     if token.text != '<EOF>':
            #         print("%s: %s" % (token.text, MetrinkLexer.symbolicNames[token.type-1]))

            parser = MetrinkParser(stream)

            parser.removeErrorListeners()
            parser.addErrorListener(MyErrorListener(l))

            tree = parser.graph_query()

            visitor = QueryBuilderVisitor()
            (start, end, expression) = visitor.visit(tree)

            print('START: ' + str(start))
            print('  END: ' + str(end))
            print('QUERY: ' + ' '.join(map(lambda a: str(a), expression)))

            # run the first function and get the DataFrame
            last_frame = expression[0].process(start, end, DataFrame())

            for i in range(1, len(expression), 2):
                conn = expression[i]
                fun = expression[i+1]

                if not isinstance(fun, QueryFunction):
                    raise ValueError('NON-QUERY FUNCTION: ' + str(fun))

                print('RUNNING: ' + str(fun))

                cur_frame = fun.process(start, end, last_frame)

                if conn == '>|': # combine the two
                    last_frame = last_frame.combine_first(cur_frame)
                else:
                    last_frame = cur_frame

                i += 2

            print("RES:")
            print(str(last_frame.head()))
            print("...")
            print(str(last_frame.tail()))

