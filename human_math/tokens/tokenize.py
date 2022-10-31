from __future__ import annotations

from collections.abc import Sequence, MutableSequence
from typing import Type

from .kind import Token, Unknown

TokenKinds = Sequence[Type[Token]]


class TokenizingError(Exception):
    pass


def first_token(expression: str, token_kinds: TokenKinds) -> Token:
    last_char = 1
    previous_candidates: TokenKinds = []
    candidates = [kind for kind in token_kinds if
                  kind.is_candidate(expression[:last_char])]  # you can't get the length of a filter object :/

    while True:
        # print(f"\nCandidates for <{expression[:last_char]}>: {candidates}")
        if len(candidates) == 0:
            if last_char > 1:
                previous_part = expression[:last_char - 1]

                valid_kinds = [kind for kind in previous_candidates if kind.is_valid(previous_part)]

                kind_number = len(valid_kinds)
                if kind_number == 0:
                    return Unknown(previous_part)
                else:
                    return valid_kinds[0](previous_part)

            else:
                return Unknown(expression[:last_char])

        elif len(candidates) == 1:
            candidate = candidates[0]

            while candidate.is_candidate(expression[:last_char + 1]):
                if last_char > len(expression):
                    break

                last_char += 1

            if candidate.is_valid(expression[:last_char]):
                return candidate(expression[:last_char])
            else:
                return Unknown(expression[:last_char])

        else:
            last_char += 1
            if last_char > len(expression):
                previous_candidates = candidates[:]
                candidates = []  # to trigger next if len(candidates) == 0 in loop
            else:
                previous_candidates = candidates[:]
                candidates = [kind for kind in token_kinds if kind.is_candidate(expression[:last_char])]


def tokenize(expression: str, token_kinds: TokenKinds, *, raise_on_unknown: bool = True,
             ignore_whitespaces: bool = True) \
        -> MutableSequence[Token]:

    tokens: list[Token] = []

    for part in expression.split():
        while len(part) != 0:
            token = first_token(part, token_kinds)

            is_unknown = isinstance(token, Unknown)

            if raise_on_unknown and is_unknown:
                raise TokenizingError(f"invalid expression \"{token.symbols}\" ")

            if len(tokens) != 0 and is_unknown and isinstance(tokens[-1], Unknown):
                tokens[-1] = Unknown(tokens[-1].symbols + token.symbols)
            else:
                tokens.append(token)

            part = part[len(token.symbols):]

    return tokens


__all__ = ["tokenize", "TokenKinds"]
