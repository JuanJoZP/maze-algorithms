import sys
import numpy as np
import pygame as pg

from time import sleep
from random import choice
from random import randint
from grid import Grid

# pygame init
pg.init()

width, height = 1000, 1000
screen = pg.display.set_mode((height, width))

bg = 125, 125, 125
screen.fill(bg)

# grid init
n_cellx, n_celly = 15, 15
wall_thick = 5
grid = Grid(screen, n_cellx, n_celly, wall_thick)
grid.color_cell(randint(2, n_cellx // 2), randint(2, n_celly // 2), 1)


# maze generation using wilson algorithm (loop erased random walk)
def loop_erased(grid: Grid, walk=[]):
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()

    grid.draw()
    sleep(0.001)
    pg.display.flip()

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if not walk:
        available = np.argwhere(np.array(grid.cell_state) == 0)
        try:
            chosen = available[0].tolist()
        except IndexError:
            return True  # maze is completed
        walk.append(chosen)
        grid.color_cell(chosen[0], chosen[1], 2)  # paints the chosen cell red

    next_pos = np.add(np.array(walk[-1]), np.array(choice(directions)))

    if np.any((next_pos < 0) | (next_pos >= grid.n_cellx)):  # if walk out of bounds
        return loop_erased(grid, walk)  # keep walking with diferent direction

    next_pos = next_pos.tolist()

    # if walk met with already created part of the maze
    if grid.cell_state[next_pos[0]][next_pos[1]] == 1:
        walk.append(next_pos)

        grid.color_cell(walk[0][0], walk[0][1], 1)
        for i in range(1, len(walk)):  # paint all the cells in the walk white
            grid.color_path((walk[i - 1][0], walk[i - 1][1]), (walk[i][0], walk[i][1]), 1)

        grid.draw()
        pg.display.flip()
        return False  # keep generating

    try:  # tries to erase loops
        intersec = walk.index(next_pos)
        for i in range(intersec + 1, len(walk)):
            grid.color_path(
                (walk[i - 1][0], walk[i - 1][1]),
                (walk[i][0], walk[i][1]),
                0,
            )

        return loop_erased(grid, walk[: intersec + 1])

    except ValueError:  # throws if no loop
        # paints the next cell red
        grid.color_path((walk[-1][0], walk[-1][1]), (next_pos[0], next_pos[1]), 2)
        walk.append(next_pos)
        return loop_erased(grid, walk)  # keep walking


while True:  # maze generation
    finished = loop_erased(grid, walk=[])
    if finished:
        break

# paints the start and the end of the maze with a red circle
grid.color_cell(0, 0, 3)
grid.color_cell(n_cellx - 1, n_celly - 1, 3)


# paints the walls

# while player has not finished
while grid.player_pos != (n_cellx - 1, n_celly - 1):
    for e in pg.event.get():
        if e.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # player movement
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_w:
                grid.move_player("up")
            if e.key == pg.K_a:
                grid.move_player("left")
            if e.key == pg.K_s:
                grid.move_player("down")
            if e.key == pg.K_d:
                grid.move_player("right")
            if e.key == pg.K_RETURN:
                break  # start auto solve

    grid.draw()
    pg.display.flip()
