from argparse import ArgumentParser, Namespace
import pathlib
import re

from dsl_info import TOKEN_REGULAR_EXPRESSIONS
from dsl_token import Token


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-p', '--program-path', type=pathlib.Path)

    return parser.parse_args()


def skip_spaces(code: str, pos: int) -> int:
    for i in range(pos, len(code)):
        if not code[i].isspace():
            return i
    return len(code)


def get_current_token(code: str, pos: int) -> tuple[Token, int]:
    for terminal, regex in TOKEN_REGULAR_EXPRESSIONS.items():
        result = re.match(regex, code[pos:])
        if not result:
            continue
        token = Token(
            type=Token.Type.TERMINAL,
            terminal_type=terminal,
            text=result.group(0)
        )
        return token, pos + len(token.text)
    raise SyntaxError(
        f'Failed to recognize token on position {pos}'
    )


def tokenize(code: str) -> list[Token]:
    size = len(code)
    pos = 0
    tokens = []
    pos = skip_spaces(code, pos)
    while pos < size:
        token, pos = get_current_token(code, pos)
        tokens.append(token)
        pos = skip_spaces(code, pos)
    return tokens


if __name__ == "__main__":
    args = parse_args()
    with open(args.program_path, 'r') as file:
        tokens = tokenize(file.read())
        print("tokens:")
        for token in tokens:
            print(f"TYPE: '{token.terminal_type}', STRING: '{token.text}'.")
