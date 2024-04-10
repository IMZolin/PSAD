from dsl_info import Nonterminal
from models import DiadelEntity, NodeParams
from utils.utils import get_id, create_connection_row


def statement_preparer(childs_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=' '.join(child_param.text for child_param in childs_params)
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


def pass_forward(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1

    return child_params[0]


def s_preparer(child_params: list[NodeParams]) -> NodeParams:
    assert len(child_params) == 1
    child_param = child_params[0]

    start_entity = DiadelEntity(name='start', id=get_id())
    end_entity = DiadelEntity(name='end', id=get_id())

    start_row = create_connection_row(start_entity, child_param.head)
    end_row = create_connection_row(child_param.tail, end_entity)

    rows = [
        start_row,
        *(child_param.rows if child_param.rows else []),
        end_row
    ]

    return NodeParams(
        head=start_entity,
        rows=rows,
        tail=end_entity,
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
    first_child_param, *other_childs_params = child_params

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


attributesMap = {
    Nonterminal.STATEMENT: statement_preparer,
    Nonterminal.OPERATOR: operator_preparer,
    Nonterminal.CODE_BLOCK: get_child_chain,
    Nonterminal.FRAGMENT: pass_forward,
    Nonterminal.ALG_UNIT_RETURN: pass_forward,
    Nonterminal.S: s_preparer,
    Nonterminal.RETURN: return_preparer,
    Nonterminal.YIELD: return_preparer,
    Nonterminal.TRANSITION: transition_preparer,
    Nonterminal.BRANCHING: branching_preparer,
    Nonterminal.FLOW_STRUCTURE: pass_forward,
}
