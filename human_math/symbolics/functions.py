import math
from abc import ABC
from collections.abc import Callable

from human_math.symbolics import FunctionNode, Node, Value


class DirectFunctionNode(FunctionNode, ABC):
    func: Callable[[float], float]

    @property
    def name(self):
        return self.func.__name__

    @classmethod
    def call(cls, arg: Node) -> Value:
        return Value(cls.func(arg.evaluate().value))


class Abs(DirectFunctionNode):
    func = abs


class Floor(DirectFunctionNode):
    func = math.floor


class Sqrt(DirectFunctionNode):
    func = math.sqrt


class Sin(DirectFunctionNode):
    func = math.sin


class Cos(DirectFunctionNode):
    func = math.cos


class Tan(DirectFunctionNode):
    func = math.tan
