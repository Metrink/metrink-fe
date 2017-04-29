import unittest

from datetime import datetime
from pandas import DataFrame

from functions.LogFunction import LogFunction


class LogFunctionTest(unittest.TestCase):
    def test_simple_query(self):
        lf = LogFunction(['logstash-2015.05.19'], {'ip': '235.60.152.170'})

        df = lf.process(datetime(2017, 1, 1), datetime(2017, 12, 31), DataFrame())

        print(df)