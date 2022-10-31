from __future__ import annotations

from collections.abc import MutableSequence, Iterable
from itertools import chain
from typing import Optional

from human_math.symbolics import Node, functions as funcs, Value
from human_math.tokens import Token
from . import parse
from .token_processor import TokenProcessor
from .tokens import OpeningParenthese, ClosingParenthese, Name, Num, Mul, Add, Sub

FUNCTIONS = {
    "abs": funcs.Abs,
    "floor": funcs.Floor,
    "sqrt": funcs.Sqrt,
    "sin": funcs.Sin,
    "cos": funcs.Cos,
    "tan": funcs.Tan
}


def get_parenthese_levels(opening_parentheses_indexes: Iterable[int],
                          closing_parentheses_indexes: Iterable[int],
                          tokens: Optional[Iterable[int]] = None) \
        -> dict[int, int]:
    if tokens is None:
        tokens = chain(opening_parentheses_indexes, closing_parentheses_indexes)

    tokens = list(tokens)

    levels = {}
    nesting_level = 0
    for p in sorted(set(chain(opening_parentheses_indexes, closing_parentheses_indexes, tokens))):
        if p in closing_parentheses_indexes:
            nesting_level -= 1

        if p in tokens:
            levels[p] = nesting_level

        if p in opening_parentheses_indexes:
            nesting_level += 1

    return levels


class Parentheses(TokenProcessor):

    @classmethod
    def get_closing_parenthese(cls, opening_parenthese_index: int, levels: dict[int, int]):
        last_parenthese = max(levels.keys())

        closing_index = opening_parenthese_index + 1

        while levels.get(closing_index, -1) != 0:
            closing_index += 1

            if closing_index > last_parenthese:
                raise parse.ParsingError(f"unmatched '(' at token {opening_parenthese_index}")

        return closing_index

    @classmethod
    def handle_parenthese(cls, index: int, token_stream: MutableSequence[Token | Node], levels: dict[int, int]) -> int:

        closing_index = cls.get_closing_parenthese(index, levels)

        content = parse.parse_tokens(token_stream[index + 1:closing_index])

        if content is None:
            token_stream[index:closing_index + 1] = []
        else:
            token_stream[index:closing_index + 1] = [content]

        return closing_index - index + (content is not None)

    @classmethod
    def handle_function(cls, index: int, token_stream: MutableSequence[Token | Node], levels: dict[int, int]) -> int:
        closing_index = cls.get_closing_parenthese(index, levels)

        func_name = token_stream[index - 1].symbols  # type: ignore

        if func_name in FUNCTIONS:
            content = parse.parse_tokens(token_stream[index + 1:closing_index])

            if content is None:
                raise parse.ParsingError(f"no argument provided to function {func_name}")
            else:
                token_stream[index - 1: closing_index + 1] = [FUNCTIONS[func_name](content)]

                return closing_index - index - 1

        else:
            raise parse.ParsingError(f"unknown function \"{func_name}\"")

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], OpeningParenthese),
                                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ClosingParenthese),
                                                                      enumerate(token_stream))))

        parentheses_levels = get_parenthese_levels(opening_parentheses_indexes, closing_parentheses_indexes)

        index_offset = 0
        for index, level in parentheses_levels.items():
            index -= index_offset
            if index in opening_parentheses_indexes and level == 0:
                if index != 0 and isinstance(token_stream[index - 1], Name):
                    index_offset += cls.handle_function(index, token_stream, parentheses_levels)
                else:
                    index_offset += cls.handle_parenthese(index, token_stream, parentheses_levels)

        return token_stream


class ImplicitMulitplication(TokenProcessor):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], OpeningParenthese),
                                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ClosingParenthese),
                                                                      enumerate(token_stream))))
        name_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Name), enumerate(token_stream))))

        levels = get_parenthese_levels(opening_parentheses_indexes, closing_parentheses_indexes,
                                       chain(opening_parentheses_indexes, name_indexes))

        offset = 0
        for index, level in levels.items():
            index += offset
            if level == 0:
                if index != 0:
                    if isinstance(token_stream[index - 1], (ClosingParenthese, Num)):
                        token_stream.insert(index, Mul('<implied>'))
                        offset += 1
                    elif (isinstance(token_stream[index - 1], Name) and token_stream[
                        index - 1].symbols not in FUNCTIONS):  # type: ignore
                        token_stream.insert(index, Mul('<implied>'))
                        offset += 1

        return token_stream


class Signs(TokenProcessor):
    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], OpeningParenthese),
                                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ClosingParenthese),
                                                                      enumerate(token_stream))))
        plus_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Add), enumerate(token_stream))))
        minus_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Sub), enumerate(token_stream))))

        levels = get_parenthese_levels(opening_parentheses_indexes, closing_parentheses_indexes,
                                       chain(plus_indexes, minus_indexes))

        offset = 0
        for index, level in levels.items():
            index += offset
            if level == 0 and index != (len(token_stream) - 1):
                if index != 0 and isinstance(token_stream[index - 1], (Num, Name, Node)):
                    continue

                if isinstance(token_stream[index + 1], Num):
                    if index in plus_indexes:
                        token_stream[index + 1].symbols = '+' + token_stream[index + 1].symbols  # type: ignore
                    else:
                        token_stream[index + 1].symbols = '-' + token_stream[index + 1].symbols  # type: ignore

                    del token_stream[index]
                    offset -= 1

                elif isinstance(token_stream[index + 1], (Name, Node)):
                    if index in plus_indexes:
                        del token_stream[index]
                        offset -= 1
                    else:
                        token_stream[index:index + 1] = [Value(-1.0), Mul("<from minus sign>")]
                        offset += 1
                else:
                    continue

        return token_stream
