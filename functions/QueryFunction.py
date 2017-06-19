from datetime import datetime
from pandas import DataFrame


class QueryFunction:
    def __init__(self, name, args):
        self.name = name
        self._args = args

    def __str__(self):
        return self.name + str(self._args)

    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        """
        Processes the function and computes the result
        :param start_time: the starting time to look at for processing
        :param end_time: the ending time to look at for processing
        :return: the result of processing this function
        """
        pass
