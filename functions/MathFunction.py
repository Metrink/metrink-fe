from datetime import datetime
from pandas import DataFrame
from functions.QueryFunction import QueryFunction


class MathFunction(QueryFunction):
    def __init__(self, name, args):
        super().__init__(name, args)

    def process(self, start_time: datetime, end_time: datetime, input:DataFrame):
        if str(self._name) not in '+-*/':
            raise ValueError("Unknown math function: " + str(self._name))

        ret = DataFrame()

        # two args means we're doing A + B
        if len(self._args) == 2:
            left = self._args[0].process(start_time, end_time, input) if isinstance(self._args[0], QueryFunction) else self._args[0]
            right = self._args[1].process(start_time, end_time, input) if isinstance(self._args[1], QueryFunction) else self._args[1]

            for l_col in left.columns:
                for r_col in right.columns:
                    if self._name == '+':
                        t = left[l_col] + right[r_col]
                    elif self._name == '-':
                        t = left[l_col] - right[r_col]
                    elif self._name == '*':
                        t = left[l_col] * right[r_col]
                    elif self._name == '/':
                        t = left[l_col] / right[r_col]
                    else:
                        raise ValueError("Unknown operator: " + str(self._name))

                    t = DataFrame(t)
                    t.columns = [l_col + self._name + r_col]

                    print(left.head())
                    print(right.head())
                    print(t.head())
                    ret = ret.combine_first(t)

        else:  # everything is in the input DataFrame
            ret = DataFrame(input.sum(axis=0))
            ret.columns = [' + '.join(input.columns)]

        return ret


class SumFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('+', args)


class MultiplyFunction(MathFunction):
    def __init__(self, name, args):
        super().__init__('*', args)
