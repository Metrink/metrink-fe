from functions.QueryFunction import QueryFunction


class MathFunction(QueryFunction):
    ADD = 0
    SUB = 1
    MUL = 2
    DIV = 3

    def __init__(self, op:int, left, right):
        if op < 0 or op > self.DIV:
            raise ValueError('Invalid operator')

        self.op = op
        self.left = left
        self.right = right

