from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import MutableSequence, Iterable, Sequence
from itertools import chain
from typing import Optional, Type

from human_math.symbolics import Node, functions as funcs, Value
from human_math.tokens import Token
from . import parse
from .token_processor import TokenProcessor
from .tokens import ParentheseOpen, ParentheseClose, Name, Num, Mul, Add, Sub, WildcardOpen, WildcardClose
from human_math.symbolics.nodes import Wildcard as Wc


FUNCTIONS = {
    "abs": funcs.Abs,
    "floor": funcs.Floor,
    "sqrt": funcs.Sqrt,
    "sin": funcs.Sin,
    "cos": funcs.Cos,
    "tan": funcs.Tan
}


def get_coupled_token_levels(opening_parentheses_indexes: Iterable[int],
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


class CoupledTokens(TokenProcessor, ABC):
    opening_token: Type[Token]
    closing_token: Type[Token]

    @classmethod
    def get_closing_token(cls, opening_token_index: int, levels: dict[int, int]) -> int:
        last_couple_token = max(levels.keys())

        closing_index = opening_token_index + 1

        while levels.get(closing_index, -1) != 0:
            closing_index += 1

            if closing_index > last_couple_token:
                raise parse.ParsingError(f"unmatched opening coupled token at token {opening_token_index}")

        return closing_index

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_tokens_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], cls.opening_token),
                                                                 enumerate(token_stream))))
        closing_tokens_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], cls.closing_token),
                                                                 enumerate(token_stream))))

        parentheses_levels = get_coupled_token_levels(opening_tokens_indexes, closing_tokens_indexes)

        index_offset = 0
        for index, level in parentheses_levels.items():

            if index in opening_tokens_indexes and level == 0:

                closing_index = cls.get_closing_token(index, parentheses_levels) - index_offset

                index -= index_offset
                block_tokens = token_stream[index + 1:closing_index]

                processed = cls.handle_block(block_tokens, token_stream, index, closing_index)
                print(f"Processed: {processed}")
                token_stream[index:closing_index + 1] = processed

                index_offset += closing_index - index + 1 - len(processed)


        return token_stream

    @classmethod
    @abstractmethod
    def handle_block(cls, tokens: Sequence[Token], token_stream: Sequence[Token | Node], opening_index: int, closing_index: int) -> Sequence[Node]:
        pass

class Parentheses(CoupledTokens):
    opening_token = ParentheseOpen
    closing_token = ParentheseClose

    @classmethod
    def handle_block(cls, tokens: Sequence[Token], token_stream: Sequence[Token | Node], opening_index: int, closing_index: int) -> Sequence[Node]:
        if opening_index != 0 and isinstance(token_stream[opening_index - 1], Name):

            return cls.handle_function(tokens, opening_index, token_stream)
        else:
            return cls.handle_parentheses(tokens)

    @classmethod
    def handle_parentheses(cls, tokens: Sequence[Token]) -> Sequence[Node]:

        content = parse.parse_tokens(tokens)

        return [] if content is None else [content]

    @classmethod
    def handle_function(cls, tokens: Sequence[Token], opening_index: int, token_stream: Sequence[Token | Node]) -> Sequence[Node]:


        func_name = token_stream[opening_index - 1].symbols  # type: ignore

        if func_name in FUNCTIONS:
            content = parse.parse_tokens(tokens)

            if content is None:
                raise parse.ParsingError(f"no argument provided to function {func_name}")

            return [FUNCTIONS[func_name](content)]

        raise parse.ParsingError(f"unknown function \"{func_name}\"")


class ImplicitMulitplication(TokenProcessor):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ParentheseOpen),
                                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ParentheseClose),
                                                                      enumerate(token_stream))))
        name_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Name), enumerate(token_stream))))

        levels = get_coupled_token_levels(opening_parentheses_indexes, closing_parentheses_indexes,
                                          chain(opening_parentheses_indexes, name_indexes))

        offset = 0
        for index, level in levels.items():
            index += offset
            if level == 0:
                if index != 0:
                    if isinstance(token_stream[index - 1], (ParentheseClose, Num)):
                        token_stream.insert(index, Mul('<implied>'))
                        offset += 1
                    elif isinstance(token_stream[index - 1], Name) and token_stream[index - 1].symbols not in FUNCTIONS:  # type: ignore
                        token_stream.insert(index, Mul('<implied>'))
                        offset += 1

        return token_stream

class Wildcard(CoupledTokens):
    opening_token = WildcardOpen
    closing_token = WildcardClose

    @classmethod
    def handle_block(cls, tokens: Sequence[Token], token_stream: Sequence[Token | Node], opening_index: int, closing_index: int) -> Sequence[Node]:
        return [Wc()]


class Signs(TokenProcessor):
    OPERATIONABLE_TOKENS = (Num, Name, Node, Wildcard)  # don't remove if operator

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ParentheseOpen),
                                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], ParentheseClose),
                                                                      enumerate(token_stream))))
        plus_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Add), enumerate(token_stream))))
        minus_indexes = list(map(lambda x: x[0], filter(lambda x: isinstance(x[1], Sub), enumerate(token_stream))))

        levels = get_coupled_token_levels(opening_parentheses_indexes, closing_parentheses_indexes,
                                          chain(plus_indexes, minus_indexes))

        offset = 0
        for index, level in levels.items():
            index += offset
            if level == 0 and index != (len(token_stream) - 1):
                if index != 0 and isinstance(token_stream[index - 1], cls.OPERATIONABLE_TOKENS):
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

