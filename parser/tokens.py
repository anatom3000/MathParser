from abc import ABC, abstractmethod
from collections.abc import MutableSequence

from parser import parse
from symbolics import BinaryOperatorNode, Node
import symbolics.operators as op
from tokens import SimpleExplcitToken, MultipleExplicitToken, Token


class ToNode(ABC):
    @classmethod
    @abstractmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        pass


class BinaryOperatorRightToLeft(ToNode):
    node: BinaryOperatorNode.__class__

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:

        operator_indexes = list(map(lambda x: x[0],
                                    filter(lambda x: type(x[1]) == cls,
                                           enumerate(token_stream))))

        for i in operator_indexes[::-1]:
            token_stream[i - 1:i + 2] = [cls.node(token_stream[i - 1], token_stream[i + 1])]

        return token_stream


class Num(Token, ToNode):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        operator_indexes = list(map(lambda x: x[0],
                                    filter(lambda x: type(x[1]) == cls,
                                           enumerate(token_stream))))

        index: int
        for index in operator_indexes:
            token_stream[index] = op.Value(float(token_stream[index].symbols))

        return token_stream

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        if symbols[0] in "+-":
            return False

        try:
            float(symbols + "0")
            return True
        except ValueError:
            return False

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        try:
            float(symbols)
            return True

        except ValueError:
            return False


class Name(Token):

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"


class Add(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '+'
    node = op.Add


class Sub(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '-'
    node = op.Sub


class Mul(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '*'
    node = op.Mul


class Div(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '/'
    node = op.Div


class Pow(MultipleExplicitToken, BinaryOperatorRightToLeft):
    names = ('**', '^')
    node = op.Pow


class Mod(MultipleExplicitToken, BinaryOperatorRightToLeft):
    names = ("mod", "%")
    node = op.Mod


class OpeningParenthese(SimpleExplcitToken, ToNode):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], OpeningParenthese),
                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], ClosingParenthese),
                                                      enumerate(token_stream))))
        parentheses_levels = {}
        nesting_level = 0
        for p in opening_parentheses_indexes + closing_parentheses_indexes:
            if p in closing_parentheses_indexes:
                nesting_level -= 1

            parentheses_levels[p] = nesting_level

            if p in opening_parentheses_indexes:
                nesting_level += 1

        try:
            last_parenthese = max(parentheses_levels.keys())
        except ValueError:
            last_parenthese = None  # we dont need the variable since next for loop wont occure (parentheses_level empty)
        for index, level in parentheses_levels.items():
            if index in opening_parentheses_indexes and level == 0:
                closing_index = index + 1
                while parentheses_levels.get(closing_index, -1) != 0:
                    closing_index += 1
                    if closing_index > last_parenthese:
                        raise parse.ParsingError(f"unmatched '(' at token {index}")
                token_stream[index:closing_index + 1] = [parse.parse(token_stream[index + 1:closing_index])]

        return token_stream

    name = "("


class ClosingParenthese(SimpleExplcitToken):
    name = ")"
