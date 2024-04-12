from dsl_info import *


def __RemoveNones(attributes):
    return [attribute for attribute in attributes if attribute]


def __Multiple(attributes):
    attributes = __RemoveNones(attributes)
    res = 1
    for num in attributes:
        res *= num
    return res


def __Add(attributes):
    attributes = __RemoveNones(attributes)
    res = 0
    for num in attributes:
        res += num
    return res

def __Vanilla(attributes):
    return "CAT"


attributesMap = {
    Nonterminal.INSTANCE : __Vanilla,
    Nonterminal.USER_CLASS : __Vanilla,
    Nonterminal.CONNECTION : __Vanilla,
}
