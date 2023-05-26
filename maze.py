from typing import List, Tuple
from random import choice, randint
import numpy as np
import time

# maze generation using wilson algorith (loop erased random walk)
def loop_erased(walk, grid):
    # ME FALTA VER SI DEPRONTO SE TROCAN X Y
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if not walk:
        zeros = np.argwhere(grid == 0)
        walk.append(zeros[np.random.randint(len(zeros))])

    next_pos = np.add(np.array(walk[-1]), np.array(choice(directions)))

    # if grid.is_active(next_pos):  # walk closed on maze
    # return walk

    if np.any((next_pos < 0) | (next_pos >= len(grid))):  # if walk out of bounds
        return loop_erased(walk, grid)  # keep walking with diferent direction

    next_pos = next_pos.tolist()

    if grid[next_pos[0]][next_pos[1]] == 1 and len(walk) > 2:
        walk.append(next_pos)
        return walk  # returns if walk closed on maze

    try:
        print(walk)
        print(next_pos)

        i = walk.index(next_pos)
        return loop_erased(walk[: i + 1], grid)  # erase loop
    except ValueError:  # throws if no loop
        walk.append(next_pos)
        return loop_erased(walk, grid)  # keep walking


grid = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
]

print(loop_erased([], grid))
