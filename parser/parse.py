from collections.abc import MutableSequence
from typing import Optional, Type

from symbolics import Node
from tokens import Token, tokenize
from .processors import Parentheses, TokenProcessor
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
    # TODO: implicit multiplication e. g. 2(3+5)
    Parentheses,
    Num,
    Pow,
    Div,
    Mul,
    Mod,
    Sub,
    Add,

]


class ParsingError(Exception):
    pass


def parse_tokens(token_stream: MutableSequence[Token | Node]) -> Optional[Node]:
    for op in TOKENS_PROCESSORS:
        token_stream = op.to_node(token_stream)

    if len(token_stream) == 0:
        return None

    if len(token_stream) != 1:
        raise ParsingError("incorrect number of nodes/tokens remaining after parsing")

    result = token_stream[0]

    if not isinstance(result, Node):
        raise ParsingError("unknown token found")

    return result


def parse(expression: str) -> Node:
    return parse_tokens(tokenize(expression, TOKENS, raise_on_unknown=False, ignore_whitespaces=True))  # type: ignore
