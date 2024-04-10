from enum import Enum
from types import MappingProxyType


class Terminal(Enum):
    WORD = "word"
    CHAR_SEQUENCE = "char_sequence"
    OTHER = 'other'


TOKEN_REGULAR_EXPRESSIONS: MappingProxyType[Terminal, str] = MappingProxyType({
    Terminal.WORD: r'[a-zA-Z0-9_+*/\-=\.]+',
    Terminal.CHAR_SEQUENCE: r'[\(\),]',
    Terminal.OTHER: r'@@{.*}'
})


KEYS: MappingProxyType[str, Terminal] = MappingProxyType({
    "algorithm": Terminal.WORD,
    "return": Terminal.WORD,
    "yield": Terminal.WORD,
    "call": Terminal.WORD,
    "func": Terminal.WORD,
    "proc": Terminal.WORD,
    "iter": Terminal.WORD,
    "assign": Terminal.WORD,
    "in": Terminal.WORD,
    "next for": Terminal.WORD,
    "exit for": Terminal.WORD,
    "define": Terminal.WORD,
    "comment": Terminal.WORD,
    "integer": Terminal.WORD,
    "string": Terminal.WORD,
    "char": Terminal.WORD,
    "array": Terminal.WORD,
    "struct": Terminal.WORD,
    "if": Terminal.WORD,
    "for": Terminal.WORD,
    "while": Terminal.WORD,
    "repeat": Terminal.WORD,
    ",": Terminal.CHAR_SEQUENCE,
    "(": Terminal.CHAR_SEQUENCE,
    ")": Terminal.CHAR_SEQUENCE,
})


class Nonterminal(Enum):
    DEFINITION = 'DEFINITION'
    INPUT = 'INPUT'
    ASSIGNMENT = 'ASSIGNMENT'
    ALG_UNIT = 'ALG_UNIT'
    WHILE = 'WHILE'
    CALL = 'CALL'
    FLOW_STRUCTURE = 'FLOW_STRUCTURE'
    FRAGMENT = 'FRAGMENT'
    REPEAT = 'REPEAT'
    RETURN = 'RETURN'
    CODE_BLOCK = 'CODE_BLOCK'
    OUTPUT = 'OUTPUT'
    BRANCHING = 'BRANCHING'
    FOR = 'FOR'
    YIELD = 'YIELD'
    NAME = 'NAME'
    COMMENT = 'COMMENT'
    TYPE_ARRAY = 'TYPE_ARRAY'
    S = 'S'
    ALG = 'ALG'
    CYCLE = 'CYCLE'
    ALG_UNIT_RETURN = 'ALG_UNIT_RETURN'
    OPERATOR = 'OPERATOR'
    TYPE = 'TYPE'
    TYPE_STRUCT = 'TYPE_STRUCT'
    TRANSITION = 'TRANSITION'
    PARAM_LIST = 'PARAM_LIST'
    STATEMENT = 'STATEMENT'
    FOR_STATEMENT = 'FOR_STATEMENT'


AXIOM = Nonterminal.S
