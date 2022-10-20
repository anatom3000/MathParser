from abc import abstractmethod, ABC
from collections.abc import MutableSequence

from . import parse, tokens
from symbolics import Node
from tokens import Token


class TokenProcessor(ABC):
    @classmethod
    @abstractmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        pass


class Parentheses(TokenProcessor):

    @classmethod
    def to_node(cls, token_stream: MutableSequence[Token | Node]) -> MutableSequence[Token | Node]:
        opening_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], tokens.OpeningParenthese),
                                                      enumerate(token_stream))))
        closing_parentheses_indexes = list(map(lambda x: x[0],
                                               filter(lambda x: isinstance(x[1], tokens.ClosingParenthese),
                                                      enumerate(token_stream))))
        parentheses_levels = {}
        nesting_level = 0
        for p in sorted(opening_parentheses_indexes + closing_parentheses_indexes):

            if p in closing_parentheses_indexes:
                nesting_level -= 1

            parentheses_levels[p] = nesting_level

            if p in opening_parentheses_indexes:
                nesting_level += 1

        try:
            last_parenthese = max(parentheses_levels.keys())
        except ValueError:
            last_parenthese = 0  # we dont need the variable since next for loop wont occure (parentheses_level empty)
        index_offset = 0
        for index, level in parentheses_levels.items():
            index -= index_offset
            if index in opening_parentheses_indexes and level == 0:
                closing_index = index + 1

                while parentheses_levels.get(closing_index, -1) != 0:
                    closing_index += 1

                    if closing_index > last_parenthese:
                        raise parse.ParsingError(f"unmatched '(' at token {index}")

                content = parse.parse_tokens(token_stream[index + 1:closing_index])
                if content is None:
                    token_stream[index:closing_index + 1] = []
                else:
                    token_stream[index:closing_index + 1] = [content]
                    index_offset += closing_index - index + 1

        return token_stream

