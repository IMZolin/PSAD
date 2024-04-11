from dataclasses import asdict
import enum

from dsl_info import Nonterminal
from models import DiadelEntity, NodeParams, IfNodeParams, ConditionBranch
from utils.utils import get_id, create_connection_row


class IfPreparerChilds(enum.Enum):
    CONDITION_IDX = 2
    TRUE_BLOCK_IDX = 5


def statement_preparer(childs_params: list[NodeParams]) -> NodeParams:
    return NodeParams(
        text=' '.join(child_param.text for child_param in childs_params)
    )


def operator_preparer(childs_params: list[NodeParams]) -> NodeParams:
    assert len(childs_params) == 1

    child_params_cls = childs_params[0].__class__
    child_params = asdict(childs_params[0])
    child_params['head'] = (
        child_params['head']
        if child_params['head']
        else DiadelEntity(
            name='action',
            id=get_id(),
            text=child_params['text'],
        )
    )

    return child_params_cls(
        **child_params
    )


def pass_forward(childs_params: list[NodeParams]) -> NodeParams:
    assert len(childs_params) == 1

    return childs_params[0]


def s_preparer(childs_params: list[NodeParams]) -> NodeParams:
    assert len(childs_params) == 1
    child_param = childs_params[0]

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


def return_preparer(childs_params: list[NodeParams]) -> NodeParams:
    assert len(childs_params) == 2

    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=' '.join(params.text for params in childs_params),
        )
    )


def transition_preparer(childs_params: list[NodeParams]) -> NodeParams:
    assert len(childs_params) == 1

    return NodeParams(
        head=DiadelEntity(
            name='action',
            id=get_id(),
            text=childs_params[0].text
        )
    )


def get_child_chain(childs_params: list[NodeParams]) -> NodeParams:
    first_child_param, *other_childs_params = childs_params

    head = first_child_param.head
    current_rows = first_child_param.rows or []
    current_tail = first_child_param.tail or head

    for child_param in other_childs_params:
        if child_param.is_key:
            continue
        conection_row = create_connection_row(current_tail, child_param.head)
        current_rows.append(conection_row)
        current_rows.extend(child_param.rows or [])
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


def branching_preparer(childs_params: list[NodeParams]) -> NodeParams:
    def slice_operators(
        childs: list[NodeParams],
        start_idx: int
    ) -> list[NodeParams]:
        operators = []
        current_idx = start_idx
        while current_idx < len(childs) and childs[current_idx].text != ')':
            if not childs[current_idx].is_key:
                operators.append(childs[current_idx])
            current_idx += 1

        return operators

    def connect_branch(
        head: DiadelEntity,
        tail: DiadelEntity,
        branch: ConditionBranch
    ) -> list[str]:
        rows = []
        rows.append(
            create_connection_row(
                head, branch.branch_params.head, branch.condition
            )
        )
        rows.extend(branch.branch_params.rows)
        rows.append(
            create_connection_row(
                branch.branch_params.tail, tail,
            )
        )

        return rows

    true_condition = childs_params[IfPreparerChilds.CONDITION_IDX.value].text
    true_operators = slice_operators(
        childs_params, IfPreparerChilds.TRUE_BLOCK_IDX.value
    )

    else_block_idx = (
        IfPreparerChilds.TRUE_BLOCK_IDX.value +
        2 * len(true_operators) - 1 +   # учитываем запятые между операторами
        3                               # всякие скобки после блока true
    )
    else_operators = slice_operators(childs_params, else_block_idx)

    true_branches = [ConditionBranch(
        branch_params=get_child_chain(true_operators),
        condition=true_condition
    )]

    # проверяем elif случай
    if (
        len(else_operators) == 1 and
        else_operators[0].head.name == 'decision' and
        else_operators[0].tail.name == 'merge'
    ):
        elif_node = else_operators[0]
        assert isinstance(elif_node, IfNodeParams)

        true_branches.extend(elif_node.true_condition_branches)
        else_branch = elif_node.else_branch
    else:
        else_branch = ConditionBranch(
            branch_params=get_child_chain(else_operators),
            condition='[else]'
        ) if else_operators else None

    head = DiadelEntity(
        name='decision',
        id=get_id(),
    )

    tail = DiadelEntity(
        name='merge',
        id=get_id(),
    )

    rows = []
    for branch in true_branches:
        rows.extend(connect_branch(head, tail, branch))

    if else_branch:
        rows.extend(connect_branch(head, tail, else_branch))
    else:
        rows.append(create_connection_row(head, tail, '[else]'))

    return IfNodeParams(
        head=head,
        rows=rows,
        tail=tail,
        true_condition_branches=true_branches,
        else_branch=else_branch
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
