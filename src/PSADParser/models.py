from pathlib import Path
from typing import Optional

from pydantic.dataclasses import dataclass

from syntax import SyntaxDescriptionType


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
