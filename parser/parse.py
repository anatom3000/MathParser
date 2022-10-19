from collections.abc import MutableSequence
from typing import Optional

from symbolics import Node
from tokens import Token, tokenize
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

TOKENS_PROCESSORS = [
    OpeningParenthese,
    Num,
    Pow,
    Mul,
    Div,
    Mod,
    Add,
    Sub,
]


class ParsingError(Exception):
    pass


def parse_tokens(token_stream: MutableSequence[Token | Node], token_processors=None) -> Optional[Node]:
    if token_processors is None:
        token_processors = TOKENS_PROCESSORS

    for op in token_processors:
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
    return parse_tokens(tokenize(expression, TOKENS, raise_on_unknown=False, ignore_whitespaces=True))
