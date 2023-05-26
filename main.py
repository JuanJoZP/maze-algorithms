import sys
import time
import pygame
from pygame import init, display, draw, event

from grid import Grid

# pygame init
init()

width, height = 1000, 1000
screen = display.set_mode((height, width))

bg = 125, 125, 125
screen.fill(bg)

# grid init
n_cellx, n_celly = 25, 25
wall_thick = 3
grid = Grid(screen, n_cellx, n_celly, wall_thick)

while True:
    for e in event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    grid.draw()

    display.flip()
