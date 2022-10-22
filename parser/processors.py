from __future__ import annotations

from collections.abc import MutableSequence, Iterable
from itertools import chain

from symbolics import Node, functions as funcs
from tokens import Token
from . import parse
from .token_processor import TokenProcessor
from .tokens import OpeningParenthese, ClosingParenthese, Name


class Parentheses(TokenProcessor):
    FUNCTIONS = {
        "abs": funcs.Abs,
        "floor": funcs.Floor,
        "sin": funcs.Sin,
        "cos": funcs.Cos,
    }

    @classmethod
    def get_parenthese_levels(cls, opening_parentheses_indexes: Iterable[int],
                              closing_parentheses_indexes: Iterable[int]) \
            -> dict[int, int]:
        levels = {}
        nesting_level = 0
        for p in sorted(chain(opening_parentheses_indexes, closing_parentheses_indexes)):

            if p in closing_parentheses_indexes:
                nesting_level -= 1

            levels[p] = nesting_level

            if p in opening_parentheses_indexes:
                nesting_level += 1

        return levels

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
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], OpeningParenthese),
                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], ClosingParenthese),
                                                      enumerate(token_stream))))

        parentheses_levels = cls.get_parenthese_levels(opening_parentheses_indexes, closing_parentheses_indexes)

        index_offset = 0
        for index, level in parentheses_levels.items():
            index -= index_offset
            if index in opening_parentheses_indexes and level == 0:
                if index != 0 and isinstance(token_stream[index - 1], Name):
                    index_offset += cls.handle_function(index, token_stream, parentheses_levels)
                else:
                    index_offset += cls.handle_parenthese(index, token_stream, parentheses_levels)

        return token_stream

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
    def handle_function(cls, index: int, token_stream: MutableSequence[Token | Node], levels: dict[int, int]) \
            -> (MutableSequence[Token | Node], int):
        offset = 0
        closing_index = cls.get_closing_parenthese(index, levels)

        func_name = token_stream[index - 1].symbols

        if func_name in cls.FUNCTIONS:
            content = parse.parse_tokens(token_stream[index + 1:closing_index])

            if content is None:
                raise parse.ParsingError(f"no argument provided to function {func_name}")
            else:
                token_stream[index - 1: closing_index + 1] = [cls.FUNCTIONS[func_name](content)]

                return closing_index - index

        else:
            raise parse.ParsingError(f"unknown function \"{func_name}\"")
