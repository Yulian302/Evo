from enum import Enum, IntEnum
from typing import Callable


class Args(IntEnum):
    UNARY = 1,
    ADD = 2,
    SUBTRACT = 2,
    MULTIPLY = 2,
    DIVIDE = 2,
    POWER = 2


class Operator:

    def __init__(self, executable: Callable, args_num: int):
        self._executable = executable
        self.args_num = args_num

    @property
    def get_args_num(self):
        return self.args_num

    def eval(self, args):
        if len(args) != self.args_num:
            return None
        return self._executable(args)


class Operators:
    UNARY_SUBTRACTION = Operator(lambda operand: -operand[0], args_num=Args.UNARY)
    ADD = Operator(lambda operands: operands[0] + operands[1], args_num=Args.ADD)
    POWER = Operator(lambda operand: operand[0] ** operand[1], args_num=Args.POWER)
    SUBTRACT = Operator(lambda operands: operands[0] - operands[1], args_num=Args.SUBTRACT)
    MULTIPLY = Operator(lambda operands: operands[0] * operands[1], args_num=Args.MULTIPLY)
    DIVIDE = Operator(lambda operands: operands[0] / operands[1], args_num=Args.DIVIDE)


class TreeLinker(Enum):
    SUM = 0,
    MAX = 1,
    MIN = 2
