import random
from enum import Enum
from typing import Tuple

import numpy as np


class OvertoneType(Enum):
    SQUARE = 1
    LINE = 2


BUTTON_TO_COORDINATES_MAPPING = {
    1: (0, 0),
    2: (0, 1),
    3: (0, 2),
    4: (1, 0),
    5: (1, 1),
    6: (1, 2),
    7: (2, 0),
    8: (2, 1),
}  # you can't use 9 by task definition


def generate_field(overtone_type: OvertoneType = None) -> np.ndarray:
    if not overtone_type:
        overtone_type = random.choice(list(OvertoneType))
    _field = np.zeros((3, 3), dtype=int)
    if overtone_type == OvertoneType.SQUARE:
        square = np.ones((2, 2), dtype=int)
        square_start = random.choice((
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ))
        _field[square_start[0]:len(square) + square_start[0], square_start[1]:len(square) + square_start[1]] = square
    elif overtone_type == OvertoneType.LINE:
        line = np.ones((3, 1), dtype=int)  # by task definition line can be only vertical
        line_start = random.choice((
            (0, 0),
            (0, 1),
            (0, 2)
        ))
        _field[0:len(line), line_start[1]:len(line[0]) + line_start[1]] = line
    return _field


def suggest_buttons() -> Tuple[int, int]:
    return 2, 8


def open_tiles(_field: np.ndarray, _buttons: Tuple[int, int]) -> np.ndarray:
    masked_field = np.chararray((3, 3), unicode=True)
    masked_field[:] = '*'
    for button in _buttons:
        coordinates = BUTTON_TO_COORDINATES_MAPPING[button]
        masked_field[coordinates] = _field[coordinates]
    return masked_field


field = generate_field()
buttons = suggest_buttons()
print(f'Suggested buttons: {buttons}')
opened = open_tiles(field, buttons)
print(f'Field after we have opened them:\n{opened}')
