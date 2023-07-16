import sys
import pygame
import numpy as np
from pygame import init, display, draw, event, key

from time import sleep
from grid import Grid
from random import choice
from random import randint

# pygame init
init()

width, height = 1000, 1000
screen = display.set_mode((height, width))

bg = 125, 125, 125
screen.fill(bg)

# grid init
n_cellx, n_celly = 15, 15
wall_thick = 5
grid = Grid(screen, n_cellx, n_celly, wall_thick)
grid.color_cell(randint(2, n_cellx // 2), randint(2, n_celly // 2), 1)

# maze generation using wilson algorithm (loop erased random walk)
def loop_erased(grid: Grid, walk=[]):
    for e in event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    grid.draw()
    sleep(0.001)
    display.flip()

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    if not walk:
        available = np.argwhere(np.array(grid.cell_state) == 0)
        try:
            chosen = available[0].tolist()
        except IndexError:
            return True  # maze is completed
        walk.append(chosen)
        grid.color_cell(chosen[0], chosen[1], 2)

    next_pos = np.add(np.array(walk[-1]), np.array(choice(directions)))

    if np.any((next_pos < 0) | (next_pos >= grid.n_cellx)):  # if walk out of bounds
        return loop_erased(grid, walk)  # keep walking with diferent direction

    next_pos = next_pos.tolist()

    if grid.cell_state[next_pos[0]][next_pos[1]] == 1:  # if walk closed on maze
        walk.append(next_pos)

        grid.color_cell(walk[0][0], walk[0][1], 1)
        for i in range(1, len(walk)):
            grid.color_path(
                (walk[i - 1][0], walk[i - 1][1]), (walk[i][0], walk[i][1]), 1
            )

        grid.draw()
        display.flip()
        return False

    try:
        intersec = walk.index(next_pos)
        for i in range(intersec + 1, len(walk)):
            grid.color_path(
                (walk[i - 1][0], walk[i - 1][1]),
                (walk[i][0], walk[i][1]),
                0,
            )

        return loop_erased(grid, walk[: intersec + 1])  # erase loop

    except ValueError:  # throws if no loop
        grid.color_path((walk[-1][0], walk[-1][1]), (next_pos[0], next_pos[1]), 2)
        walk.append(next_pos)
        return loop_erased(grid, walk)  # keep walking


while True:
    finished = loop_erased(grid, walk=[])
    if finished:
        break

grid.color_cell(0, 0, 3)
grid.color_cell(n_cellx - 1, n_celly - 1, 3)

# colorear las paredes si estan en 1

while grid.player_pos != (n_cellx - 1, n_celly - 1):
    for e in event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_w:
                grid.move_player("up")
            if e.key == pygame.K_a:
                grid.move_player("left")
            if e.key == pygame.K_s:
                grid.move_player("down")
            if e.key == pygame.K_d:
                grid.move_player("right")
            if e.key == pygame.K_RETURN:
                break  # start auto solve

    grid.draw()
    display.flip()

while grid.player_pos != (n_cellx - 1, n_celly - 1):
    pass
    # crear un metodo que mire las casillas libres aledañas
    # agregar las casillas aledañas a una pila
    # mover el jugador a la casilla siguiente en la pila
