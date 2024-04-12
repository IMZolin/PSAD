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
    ALG = 'ALG'
    ALG_UNIT = 'ALG_UNIT'
    ALG_UNIT_RETURN = 'ALG_UNIT_RETURN'
    ASSIGNMENT = 'ASSIGNMENT'
    BRANCHING = 'BRANCHING'
    CALL = 'CALL'
    CODE_BLOCK = 'CODE_BLOCK'
    COMMENT = 'COMMENT'
    CYCLE = 'CYCLE'
    DEFINITION = 'DEFINITION'
    FLOW_STRUCTURE = 'FLOW_STRUCTURE'
    FOR = 'FOR'
    FOR_STATEMENT = 'FOR_STATEMENT'
    FRAGMENT = 'FRAGMENT'
    INPUT = 'INPUT'
    NAME = 'NAME'
    OPERATOR = 'OPERATOR'
    OUTPUT = 'OUTPUT'
    PARAM_LIST = 'PARAM_LIST'
    REPEAT = 'REPEAT'
    RETURN = 'RETURN'
    S = 'S'
    STATEMENT = 'STATEMENT'
    TRANSITION = 'TRANSITION'
    TYPE = 'TYPE'
    TYPE_ARRAY = 'TYPE_ARRAY'
    TYPE_STRUCT = 'TYPE_STRUCT'
    YIELD = 'YIELD'
    WHILE = 'WHILE'


AXIOM = Nonterminal.S
