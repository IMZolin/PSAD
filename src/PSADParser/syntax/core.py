from enum import Enum
from pathlib import Path

from pydantic.dataclasses import dataclass


class SyntaxDescriptionType(Enum):
    VIRT_DIAGRAMS = "virt"
    RBNF = "rbnf"


class NodeType(Enum):
    TERMINAL = 0
    KEY = 1
    NONTERMINAL = 2
    START = 3
    END = 4


class Node:
    def __init__(self, type, str):
        self.type = type
        self.str = str
        self.nextNodes = []


@dataclass
class SyntaxInfo:
    type: SyntaxDescriptionType
    diagrams_path: Path
