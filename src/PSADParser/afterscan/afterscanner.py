from collections import defaultdict
from typing import Callable

from dsl_info import KEYS, Terminal
from dsl_token import Token
from models import NodeParams


def apply_converter(
    tokens: list[Token],
    converter: Callable[[Token], list[Token]]
) -> list[Token]:
    res = []
    for token in tokens:
        res.extend(converter(token))
    return res


def replace_keywords(
    terminal_map: dict[Terminal, list[str]],
    token: Token
) -> list[Token]:
    if (
        token.type == Token.Type.TERMINAL and
        token.terminal_type in terminal_map and
        token.text in terminal_map[token.terminal_type]
    ):
        token.type = Token.Type.KEY

    return [token]


def set_attributes(tokens: list[Token]) -> None:
    for token in tokens:
        token.attribute = NodeParams(
            text=(
                token.text
                if token.terminal_type != Terminal.OTHER
                else ' '.join(
                    word.removeprefix('@@{').removesuffix('}')
                    for word in token.text.split()
                )
            ),
            is_key=token.type == Token.Type.KEY
        )


def afterscan(tokens: list[Token]):
    terminal_map = defaultdict(list)
    for key, terminal in KEYS.items():
        terminal_map[terminal].append(key)

    converted_tokens = apply_converter(
        tokens=tokens,
        converter=lambda token: replace_keywords(terminal_map, token),
    )
    set_attributes(converted_tokens)

    return converted_tokens
