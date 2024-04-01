from typing import Optional

from models import DiadelEntity


ENTITY_ID = 0

def get_id():
    global ENTITY_ID
    ENTITY_ID += 1
    return ENTITY_ID


def create_connection_row(
    right: DiadelEntity,
    left: DiadelEntity,
    text: Optional[str] = None
) -> str:
    connection_text = f'{{text={text}}}' if text else ''

    return f'{right.to_string()} =>{connection_text} {left.to_string()}'
