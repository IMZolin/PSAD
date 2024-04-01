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


def code_block_preparer(child_params: list[NodeParams]) -> NodeParams:
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


def fragment_preparer(child_params: list[NodeParams]) -> NodeParams:
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


attributesMap = {
    Nonterminal.STATEMENT: statement_preparer,
    Nonterminal.OPERATOR: operator_preparer,
    Nonterminal.CODE_BLOCK: code_block_preparer,
    Nonterminal.FRAGMENT: fragment_preparer,
    Nonterminal.S: s_preparer,
}
