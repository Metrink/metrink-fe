import unittest

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from parser.MetrinkFrontendLexer import MetrinkFrontendLexer
from parser.MetrinkFrontendParser import MetrinkFrontendParser

from QueryBuilderVisitor import QueryBuilderVisitor


class MyErrorListener(ErrorListener, unittest.TestCase):
    def __init__(self, input):
        super().__init__()
        self.input = input

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("LINE: %s" % self.input)
        print("%d:%d %s" % (line, column, msg))
        self.fail("PARSE FAILED")

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print(str(startIndex) + " to " + str(stopIndex))


class MetrinkParserTest(unittest.TestCase):
    def create_token_stream(self, line):
        istream = InputStream(line)
        lexer = MetrinkFrontendLexer(istream)
        stream = CommonTokenStream(lexer)

        stream.fill()

        return stream

    def parse_file(self, input_file, debug=False):
        """
        Given a file filled with a query-per-line, parse the file
        :param input_file: the file to parse
        :param debug: True will print out the full token list
        """
        with open(input_file, 'r') as f:
            for l in f:
                l = l.rstrip()

                if len(l) < 2:
                    continue

                if l.startswith("#"):
                    continue

                if debug:
                    print('INPUT: ' + l)

                stream = self.create_token_stream(l)

                if debug:
                    for token in stream.tokens:
                        if token.text != '<EOF>':
                            print("%s: %s" % (token.text, MetrinkFrontendLexer.symbolicNames[token.type - 1]))

                parser = MetrinkFrontendParser(stream)

                parser.removeErrorListeners()
                parser.addErrorListener(MyErrorListener(l))

                parser.metrink_query()

    def test_valid_metric(self):
        query = "-1d metric(f1: 7, f2: ['a', 'b'], f3: {s*t})"
        stream = self.create_token_stream(query)
        parser = MetrinkFrontendParser(stream)

        parser.removeErrorListeners()
        parser.addErrorListener(MyErrorListener(query))

        tree = parser.metrink_query()

        visitor = QueryBuilderVisitor()

        (start, end, expression) = visitor.visit(tree)

        print('START: ' + str(start))
        print('  END: ' + str(end))
        print('QUERY: ' + ' '.join(map(lambda a: str(a), expression)))


