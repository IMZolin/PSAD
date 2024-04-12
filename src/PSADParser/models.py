from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class DiadelEntity:
    name: str
    id: int
    text: Optional[str] = None

    def to_string(self) -> str:
        params = ', '.join(
            (
                f'id={self.id}',
                f'text="{self.text}"' if self.text else ''
            )
        )

        if params.endswith(', '):
            params = params[:-2]

        return f'{self.name}{{{params}}}'


@dataclass
class NodeParams:
    text: Optional[str] = None
    rows: Optional[list[str]] = None
    head: Optional[DiadelEntity] = None
    tail: Optional[DiadelEntity] = None
    is_key: bool = False


@dataclass
class ConditionBranch:
    branch_params: NodeParams
    condition: str


@dataclass
class IfNodeParams(NodeParams):
    true_condition_branches: Optional[list[ConditionBranch]] = None
    else_branch: Optional[ConditionBranch] = None
