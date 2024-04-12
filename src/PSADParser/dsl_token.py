from dsl_info import Terminal
from enum import Enum


class Token:
    class Type(Enum):
        TERMINAL = 0
        KEY = 1

    def __init__(self, type: Type, terminal_type: Terminal, text: str):
        self.type = type
        self.terminal_type = terminal_type
        self.text = text
        self.attribute = None
