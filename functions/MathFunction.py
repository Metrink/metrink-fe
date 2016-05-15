from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class MathFunction(QueryFunction):
    def __init__(self, name, args):
        super().__init__(name, args)

        if len(args) < 2:
            raise ValueError("Must have at least 2 args for math functions: " + str(args))

    def process(self, start_time: datetime, end_time: datetime, input:DataFrame):
        if len(self._args) == 1:
            left = input
            i = 0
        else:
            left = self._args[0].process(start_time, end_time, input) if isinstance(self._args[0], QueryFunction) else self._args[0]
            i = 1

        while i < len(self._args):
            right = self._args[i].process(start_time, end_time, input) if isinstance(self._args[i], QueryFunction) else self._args[i]

            if self._name == '+':
                left = left + right
            elif self._name == '-':
                left = left - right
            elif self._name == '*':
                left = left * right
            elif self._name == '/':
                left = left / right
            else:
                raise ValueError("Unknown math function: " + str(self._name))

            i += 1

        return left


class SumFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('+', args)


class MultiplyFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('*', args)
