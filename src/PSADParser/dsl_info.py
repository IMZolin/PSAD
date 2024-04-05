from enum import Enum


class Terminal(Enum):
    word = "word"
    char_sequence = "char_sequence"
    other = 'other'


tokenRegularExpressions = [
    (Terminal.word, r'[a-zA-Z0-9_+*/\-=\.]+'),
    (Terminal.char_sequence, r'[\(\),]'),
    (Terminal.other, r'@@{.*}')
]


keys = [
    ("algorithm", Terminal.word),
    ("return", Terminal.word),
    ("yield", Terminal.word),
    ("call", Terminal.word),
    ("func", Terminal.word),
    ("proc", Terminal.word),
    ("iter", Terminal.word),
    ("assign", Terminal.word),
    ("next for", Terminal.word),
    ("exit for", Terminal.word),
    ("define", Terminal.word),
    ("comment", Terminal.word),
    ("integer", Terminal.word),
    ("string", Terminal.word),
    ("char", Terminal.word),
    ("array", Terminal.word),
    ("struct", Terminal.word),
    ("if", Terminal.word),
    ("for", Terminal.word),
    ("while", Terminal.word),
    ("repeat", Terminal.word),
    (",", Terminal.char_sequence),
    ("(", Terminal.char_sequence),
    (")", Terminal.char_sequence),
]


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


axiom = Nonterminal.S
