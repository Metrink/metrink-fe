from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class MathFunction(QueryFunction):
    def __init__(self, name, args):
        super().__init__(name, args)

        if len(args) < 2:
            raise ValueError("Must have at least 2 args for math functions: " + str(args))

    def process(self, start_time: datetime, end_time: datetime, input:DataFrame):
        """
        Processes the function and computes the result
        :param start_time: the starting time to look at for processing
        :param end_time: the ending time to look at for processing
        :return: the result of processing this function
        """
        pass


class SumFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('+', args)


class MultiplyFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('*', args)
