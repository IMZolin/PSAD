import re
import itertools
from dsl_info import Nonterminal
from models import DiadelEntity, NodeParams
from utils.utils import get_id, create_connection_row


def statement_preparer(childs_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=' '.join(child_param.text for child_param in childs_params)
    )


def assignment_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 6
    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=''.join(child_params[2].text + ":=" + child_params[4].text),
        )
    )


def call_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 6
    print()
    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=''.join([child_params[2].text, child_params[4].text])
        )
    )


def param_list_preparer(child_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=''.join(params.text for params in child_params)
    )


def input_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 3
    return NodeParams(
        text=''.join(params.text for params in child_params)
    )


def definition_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 6
    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=': '.join([child_params[2].text, child_params[4].text]),
        )
    )


def type_array_preparer(child_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=''.join([child_params[0].text, '[' + child_params[2].text + ']'])
    )


def type_struct_preparer(child_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=''.join([child_params[0].text, '{' + child_params[2].text + '}'])
    )


def operator_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1
    child_param = child_params[0]
    child_head = (
        child_param.head
        if child_param.head
        else DiadelEntity(
            name='action',
            id=get_id(),
            text=child_param.text,
        )
    )

    return NodeParams(
        head=child_head,
        rows=child_param.rows,
    )


def code_block_preparer(child_params: list[NodeParams]) -> NodeParams:
    operations_list = []
    functions_list = []
    current_rows = []
    head = None
    current_tail = None

    for child_param in child_params:
        if child_param.head.name.startswith('comment'):
            functions_list.append(child_param)
        else:
            operations_list.append(child_param)
    if operations_list:
        first_child_param, *other_childs_params = operations_list
        head = first_child_param.head
        current_rows.extend(first_child_param.rows or [])
        current_tail = first_child_param.tail or head

        for child_param in other_childs_params:
            if child_param.is_key:
                continue
            conection_row = create_connection_row(current_tail, child_param.head)
            current_rows.append(conection_row)
            current_tail = (
                child_param.tail
                if child_param.tail
                else child_param.head
            )

    for fun in functions_list:
        current_rows.extend(fun.rows)
    # current_rows.extend(itertools.chain.from_iterable(fun.rows for fun in functions_list))

    return NodeParams(
        rows=current_rows,
        head=head,
        tail=current_tail,
    )


def pass_forward(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1
    return child_params[0]


def s_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1
    child_param = child_params[0]
    start_entity = None
    end_entity = None
    if child_param.head:
        start_entity = DiadelEntity(name='start', id=get_id())
        end_entity = DiadelEntity(name='end', id=get_id())

        start_row = create_connection_row(start_entity, child_param.head)
        end_row = create_connection_row(child_param.tail, end_entity)

        rows = [
            start_row,
            *(child_param.rows if child_param.rows else []),
            end_row
        ]
    else:
        rows = child_param.rows
    return NodeParams(
        head=start_entity,
        rows=rows,
        tail=end_entity
    )


def return_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 2
    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=' '.join(params.text for params in child_params),
        )
    )


def transition_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1
    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=child_params[0].text
        )
    )


def get_child_chain(child_params: list[NodeParams]) -> NodeParams:
    if len(child_params) > 1:
        first_child_param, *other_childs_params = child_params
    else:
        first_child_param = child_params[0]
        other_childs_params = []

    head = first_child_param.head
    current_rows = first_child_param.rows or []
    current_tail = first_child_param.tail or head

    for child_param in other_childs_params:
        if child_param.is_key:
            continue
        conection_row = create_connection_row(current_tail, child_param.head)
        current_rows.append(conection_row)
        current_tail = (
            child_param.tail
            if child_param.tail
            else child_param.head
        )

    return NodeParams(
        rows=current_rows,
        head=head,
        tail=current_tail,
    )


def branching_preparer(child_params: list[NodeParams]) -> NodeParams:
    condition = child_params[2]

    true_operations = []
    current_true_idx = 5
    while not child_params[current_true_idx].is_key:
        true_operations.append(child_params[current_true_idx])
        current_true_idx += 1

    else_operations = []
    current_else_idx = current_true_idx + 3
    while not child_params[current_else_idx].is_key:
        else_operations.append(child_params[current_else_idx])
        current_else_idx += 1
    true_block = get_child_chain(true_operations)
    else_block = get_child_chain(else_operations)

    head = DiadelEntity(
        name='decision',
        id=get_id(),
    )
    tail = DiadelEntity(
        name='merge',
        id=get_id(),
    )
    rows = []
    rows.append(create_connection_row(
        head, true_block.head, text=condition.text)
    )
    rows.extend(true_block.rows)
    rows.append(create_connection_row(
        true_block.tail, tail,
    ))

    if else_block.head:
        rows.append(create_connection_row(
            head, else_block.head, text='[else]',
        ))
        rows.extend(else_block.rows)
        rows.append(create_connection_row(
            else_block.tail, tail
        ))
    else:
        rows.append(create_connection_row(
            head, tail, text='[else]',
        ))
    
    return NodeParams(
        head=head,
        rows=rows,
        tail=tail,
    )


def while_preparer(child_params: list[NodeParams]) -> NodeParams:
    condition = child_params[2]
    current_idx = 4
    operations = []
    while not child_params[current_idx].text == ')':
        operations.append(child_params[current_idx])
        current_idx += 1
    block = get_child_chain(operations)
    head = DiadelEntity(
        name='decision',
        id=get_id(),
    )
    rows=[]
    rows.extend(
        [create_connection_row(head, block.head, text=condition.text), create_connection_row(block.tail, head)]
    )
    rows.extend(block.rows)
    return NodeParams(
        head=head,
        rows=rows
    )


def for_statement_preparer(child_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=','.join([child_params[0].text, child_params[2].text])
    )


def for_preparer(child_params: list[NodeParams]) -> NodeParams:
    elem, collection = child_params[2].text.split(',')
    condition = collection + ' isn`t empty'

    rows = []
    next_elem = DiadelEntity(name="action", id=get_id(), text=elem + " := next(" + collection + ")")

    current_idx = 4
    operations = []
    head = DiadelEntity(
        name='decision',
        id=get_id(),
    )
    while not child_params[current_idx].text == ')':
        operations.append(child_params[current_idx])
        current_idx += 1
    block = get_child_chain(operations)
    rows.extend([create_connection_row(head, next_elem, condition), create_connection_row(next_elem, block.head)])
    rows.extend(block.rows)
    rows.append(create_connection_row(block.tail, head))

    return NodeParams(
        head=head,
        rows=rows
    )


def alg_unit_preparer(child_params: list[NodeParams]) -> NodeParams:
    alg_key = child_params[0]
    alg_name = child_params[2]
    alg_input = child_params[4]
    current_idx = 6
    operations = []
    rows = []
    while not child_params[current_idx].text == ')':
        operations.append(child_params[current_idx])
        current_idx += 1
    block = get_child_chain(operations)
    oper_block = s_preparer([block])
    fun_name = DiadelEntity(name="comment", id=get_id(), text=f"{alg_key.text}{alg_name.text}{alg_input.text}")
    rows.extend([create_connection_row(fun_name, oper_block.head)])
    rows.extend(oper_block.rows)
    return NodeParams(
        head=fun_name,
        rows=rows
    )


attributesMap = {
    Nonterminal.STATEMENT: statement_preparer,
    Nonterminal.OPERATOR: operator_preparer,
    Nonterminal.CODE_BLOCK: code_block_preparer,
    Nonterminal.FRAGMENT: pass_forward,
    Nonterminal.ALG_UNIT_RETURN: pass_forward,
    Nonterminal.S: s_preparer,
    Nonterminal.RETURN: return_preparer,
    Nonterminal.YIELD: return_preparer,
    Nonterminal.TRANSITION: transition_preparer,
    Nonterminal.BRANCHING: branching_preparer,
    Nonterminal.FLOW_STRUCTURE: pass_forward,
    Nonterminal.ASSIGNMENT: assignment_preparer,
    Nonterminal.NAME: pass_forward,
    Nonterminal.TYPE: pass_forward,
    Nonterminal.OUTPUT: pass_forward,
    Nonterminal.TYPE_ARRAY: type_array_preparer,
    Nonterminal.TYPE_STRUCT: type_struct_preparer,
    Nonterminal.DEFINITION: definition_preparer,
    Nonterminal.INPUT: input_preparer,
    Nonterminal.PARAM_LIST: param_list_preparer,
    Nonterminal.CALL: call_preparer,
    Nonterminal.CYCLE: pass_forward,
    Nonterminal.WHILE: while_preparer,
    Nonterminal.FOR: for_preparer,
    Nonterminal.FOR_STATEMENT: for_statement_preparer,
    Nonterminal.ALG_UNIT: alg_unit_preparer
}
