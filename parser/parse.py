from collections.abc import MutableSequence

from symbolics import Node
from tokens import Token
from .tokens import Add, Sub, Pow, Num, Mul, Div, Mod, OpeningParenthese


class ParsingError(Exception):
    pass


OPERATORS = [
    OpeningParenthese,
    Num,
    Pow,
    Mul,
    Div,
    Mod,
    Add,
    Sub,
]


def parse(token_stream: MutableSequence[Token | Node], token_processors=None):

    if token_processors is None:
        token_processors = OPERATORS

    for op in token_processors:
        token_stream = op.to_node(token_stream)

    if len(token_stream) != 1:
        raise ParsingError("incorrect number of nodes/tokens remaining after parsing")

    result = token_stream[0]

    if not isinstance(result, Node):
        raise ParsingError("unknown token found")

    return result
