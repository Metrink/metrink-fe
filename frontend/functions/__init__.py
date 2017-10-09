from frontend.functions.AbsoluteValueFunction import AbsoluteValueFunction
from frontend.functions.AverageFunction import AverageFunction
from frontend.functions.GraphFunction import GraphFunction
from frontend.functions.MovingAverageFunction import MovingAverageFunction
from frontend.functions.MathFunction import MultiplyFunction
from frontend.functions.MathFunction import SumFunction


QUERY_FUNCTIONS = {
    'abs': AbsoluteValueFunction,
    'avg': AverageFunction,
    'graph': GraphFunction,
    'mavg': MovingAverageFunction,
    'mul': MultiplyFunction,
    'sum': SumFunction,
}