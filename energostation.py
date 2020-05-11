from pprint import pprint

import numpy as np

MAX_HEIGHT = 5
MAX_WIDTH = 5
DESIRED_SUM = 15

CACHED_LAYOUT = np.array([
    [5, 3, 2, 4, 1],
    [3, 4, 1, 2, 5],
    [1, 2, 3, 5, 4],
    [2, 5, 4, 1, 3],
    [4, 1, 5, 3, 2]
])


def init_layout() -> np.ndarray:
    _layout = np.empty((MAX_HEIGHT, MAX_WIDTH), dtype=int)
    for i in range(MAX_HEIGHT):
        _layout[i] = np.arange(1, MAX_HEIGHT + 1)
    return _layout


def shuffle_layout(_layout: np.ndarray) -> np.ndarray:
    for line in _layout:
        np.random.shuffle(line)
    return _layout


def layout_is_valid(_layout: np.ndarray) -> bool:
    if len(_layout) != MAX_HEIGHT:
        print(f'Layout gone wrong: height is not {MAX_HEIGHT}')
        return False

    for i, line in enumerate(_layout):
        if len(line) != MAX_WIDTH:
            print(f'Layout gone wrong: line {i + 1} width != {MAX_WIDTH}')
            return False

    for i, line in enumerate(_layout):
        if len(line) != len(set(line)):
            print(f'Layout gone wrong: line {i + 1} has duplicates')
            return False

    for i in range(MAX_HEIGHT):
        column = [line[i] for line in _layout]
        if len(column) != len(set(column)):
            print(f'Layout gone wrong: column {i + 1} has duplicates')
            return False

    for i, line in enumerate(_layout):
        if sum(line) != DESIRED_SUM:
            print(f'Layout gone wrong: line {i + 1} sum {sum(line)} != {DESIRED_SUM}')
            return False

    for i in range(MAX_HEIGHT):
        column = [line[i] for line in _layout]
        if sum(column) != DESIRED_SUM:
            print(f'Layout gone wrong: column {i + 1} sum {sum(column)} != {DESIRED_SUM}')
            return False

    main_diagonal = np.diag(_layout)
    if sum(main_diagonal) != DESIRED_SUM:
        print(f'Layout gone wrong: main diagonal sum {sum(main_diagonal)} != {DESIRED_SUM}')
        return False

    if len(main_diagonal) != len(set(main_diagonal)):
        print(f'Layout gone wrong: main diagonal has duplicates')
        return False

    secondary_diagonal = np.diag(np.fliplr(_layout))
    if sum(secondary_diagonal) != DESIRED_SUM:
        print(f'Layout gone wrong: secondary diagonal sum {sum(secondary_diagonal)} != {DESIRED_SUM}')
        return False

    if len(secondary_diagonal) != len(set(secondary_diagonal)):
        print(f'Layout gone wrong: secondary diagonal has duplicates')
        return False

    print('Layout is valid.')
    return True


def brute_force() -> np.ndarray:
    layout = init_layout()
    layout = shuffle_layout(layout)
    iteration = 1
    while not layout_is_valid(layout):
        print(f'Trying another layout, iteration #{iteration} ..')
        iteration += 1
        layout = shuffle_layout(layout)
    return layout


def solve():
    if CACHED_LAYOUT is not None:
        pprint(CACHED_LAYOUT)
    else:
        pprint(brute_force())


solve()
