import unittest

from antlr4 import InputStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener

from parser.MetrinkLexer import MetrinkLexer
from parser.MetrinkParser import MetrinkParser


class MyErrorListener(ErrorListener, unittest.TestCase):
    def __init__(self, input):
        self.input = input

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("FAILED: %s" % self.input)
        self.fail("PARSE FAILED:\t %d:%d %s" % (line, column, msg))

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        print(str(startIndex) + " to " + str(stopIndex))


class MetrinkParserTest(unittest.TestCase):
    def create_token_stream(self, line):
        istream = InputStream(line)
        lexer = MetrinkLexer(istream)
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
                            print("%s: %s" % (token.text, MetrinkLexer.symbolicNames[token.type - 1]))

                parser = MetrinkParser(stream)

                parser.removeErrorListeners()
                parser.addErrorListener(MyErrorListener(l))

                parser.metrink_query()

    def test_valid_queries(self):
        self.parse_file('valid_queries.txt')

