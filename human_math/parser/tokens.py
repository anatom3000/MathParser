from __future__ import annotations

import math
from collections.abc import MutableSequence
from typing import Type

import human_math.symbolics.operators as op
from .token_processor import TokenProcessor
from human_math.symbolics import BinaryOperatorNode, Node
from human_math.tokens import SimpleExplcitToken, MultipleExplicitToken, Token


class BinaryOperatorRightToLeft(TokenProcessor):
    node: Type[BinaryOperatorNode]

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        operator_indexes = list(map(lambda x: x[0], filter(lambda x: type(x[1]) == cls, enumerate(token_stream))))

        for i in operator_indexes[::-1]:
            token_stream[i - 1:i + 2] = [cls.node(token_stream[i - 1], token_stream[i + 1])]  # type: ignore

        return token_stream


class BinaryOperatorLeftToRight(TokenProcessor):
    node: Type[BinaryOperatorNode]

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        operator_indexes = list(map(lambda x: x[0], filter(lambda x: type(x[1]) == cls, enumerate(token_stream))))

        index_offset = 0
        for i in operator_indexes:
            i -= index_offset
            token_stream[i - 1:i + 2] = [cls.node(token_stream[i - 1], token_stream[i + 1])]  # type: ignore
            index_offset += 2

        return token_stream


class Num(Token, TokenProcessor):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        operator_indexes = list(map(lambda x: x[0], filter(lambda x: type(x[1]) == cls, enumerate(token_stream))))

        index: int
        for index in operator_indexes:
            token_stream[index] = op.Value(float(token_stream[index].symbols))  # type: ignore

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


class Name(Token, TokenProcessor):
    CONSTANTS = {
        "pi": op.Constant(math.pi, "pi"),
        "tau": op.Constant(math.tau, "tau"),
        "e": op.Constant(math.e, "e"),
        "inf": op.Constant(math.inf, "Infinity")
    }

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        operator_indexes = list(filter(lambda x: type(x[1]) == cls, enumerate(token_stream)))

        index: int
        for index, token in operator_indexes:
            if token.symbols in cls.CONSTANTS:  # type: ignore
                token_stream[index] = cls.CONSTANTS[token.symbols]  # type: ignore
            else:
                token_stream[index] = op.Variable(token_stream[index].symbols)  # type: ignore

        return token_stream

    @classmethod
    def is_candidate(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"

    @classmethod
    def is_valid(cls, symbols: str) -> bool:
        return symbols.isalnum() and symbols[0] not in "0123456789"


class Add(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '+'
    node = op.Add


class Sub(SimpleExplcitToken, BinaryOperatorLeftToRight):
    name = '-'
    node = op.Sub


class Mul(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = '*'
    node = op.Mul


class Div(SimpleExplcitToken, BinaryOperatorLeftToRight):
    name = '/'
    node = op.Div


class Pow(MultipleExplicitToken, BinaryOperatorRightToLeft):
    names = ('**', '^')
    node = op.Pow


class Mod(SimpleExplcitToken, BinaryOperatorRightToLeft):
    name = "%"
    node = op.Mod


class OpeningParenthese(SimpleExplcitToken):
    name = "("


class ClosingParenthese(SimpleExplcitToken):
    name = ")"

