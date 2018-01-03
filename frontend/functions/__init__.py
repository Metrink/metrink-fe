from functions.AbsoluteValueFunction import AbsoluteValueFunction
from functions.AverageFunction import AverageFunction
from functions.GraphFunction import GraphFunction
from functions.MovingAverageFunction import MovingAverageFunction
from functions.MathFunction import MultiplyFunction
from functions.MathFunction import SumFunction


QUERY_FUNCTIONS = {
    'abs': AbsoluteValueFunction,
    'avg': AverageFunction,
    'graph': GraphFunction,
    'mavg': MovingAverageFunction,
    'mul': MultiplyFunction,
    'sum': SumFunction,
}