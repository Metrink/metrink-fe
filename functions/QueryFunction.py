from datetime import datetime


class QueryFunction:
    def __init__(self, name, args):
        self._name = name
        self._args = args

    def __str__(self):
        return self._name + str(self._args)

    def process(self, start_time:datetime, end_time:datetime):
        """
        Processes the function and computes the result
        :param start_time: the starting time to look at for processing
        :param end_time: the ending time to look at for processing
        :return: the result of processing this function
        """
        pass
