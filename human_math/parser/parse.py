from __future__ import annotations

from collections.abc import MutableSequence
from typing import Optional, Type

from human_math.symbolics import Node
from human_math.tokens import Token, tokenize
from .processors import Parentheses, TokenProcessor, ImplicitMulitplication, Signs
from .tokens import Add, Sub, Pow, Num, Mul, Div, Mod, OpeningParenthese, ClosingParenthese, Name

TOKENS = [
    Num,
    Add,
    Sub,
    Mul,
    Div,
    Pow,
    Mod,
    OpeningParenthese,
    ClosingParenthese,
    Name,
]

TOKENS_PROCESSORS: list[Type[TokenProcessor]] = [
    ImplicitMulitplication,
    Parentheses,
    Signs,
    Num,
    Name,
    Pow,
    Div,
    Mul,
    Mod,
    Sub,
    Add
]


class ParsingError(Exception):
    pass


def parse_tokens(token_stream: MutableSequence[Token | Node]) -> Optional[Node]:
    for op in TOKENS_PROCESSORS:
        token_stream = op.to_node(token_stream)

    if len(token_stream) == 0:
        return None

    if len(token_stream) != 1:
        # print(token_stream)
        # raise ParsingError("incorrect number of nodes/tokens remaining after parsing")
        pass

    result = token_stream[0]

    if not isinstance(result, Node):
        raise ParsingError(f"unknown token found {result}")

    return result


def parse(expression: str) -> Node:
    return parse_tokens(tokenize(expression, TOKENS, raise_on_unknown=False, ignore_whitespaces=True))  # type: ignore
