from datetime import datetime
from pandas import DataFrame

from functions.QueryFunction import QueryFunction


class AbsoluteValueFunction(QueryFunction):
    def process(self, start_time:datetime, end_time:datetime, input:DataFrame):
        if (self._args is not None and len(self._args) > 2) or \
           (len(self._args) != 0 and not isinstance(self._args[0], QueryFunction)):
            raise ValueError('Invalid argument to absolute value function')

        # get the data
        data = input if len(self._args) == 0 else self._args[0].process(start_time, end_time, input)

        ret = None

        # go through each column, get the average, and apply it to the rows
        for col in data.columns:
            abs = data[col].abs()  # get the absolute value for each value in the column
            abs.name = 'abs ' + col  # update the name

            if ret is None:
                ret = DataFrame(abs)
            else:
                ret = ret.combine_first(DataFrame(abs))  # add it to our return value

        print(ret.head())

        return ret
