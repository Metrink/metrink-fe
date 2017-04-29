import unittest

from datetime import datetime
from pandas import DataFrame

from functions.LogFunction import LogFunction


class LogFunctionTest(unittest.TestCase):
    def test_simple_query(self):
        lf = LogFunction(['test'], {'f1': 'blah'})

        df = DataFrame()

        lf.process(datetime(2017, 1, 1), datetime(2017, 12, 31), df)

        print(df)