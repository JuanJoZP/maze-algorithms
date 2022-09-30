import pygame as pg
import numpy as np
import matplotlib.pyplot as plt
from maze import randomwalk2D

BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
POINT_SIZE = 15
TOP = 200
LEFT = 250
MAZE_MAX = 30


class Point(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pg.Surface([POINT_SIZE, POINT_SIZE])
        self.color = BLACK
        self.image.fill(self.color)

        self.x = x
        self.y = y
        self.rect = self.image.get_rect()
        self.rect.x = LEFT + x*(POINT_SIZE)
        self.rect.y = TOP + y*(POINT_SIZE)

    def change_color(self):
        self.color = BLACK if self.color == WHITE else WHITE
        self.image.fill(self.color)


def main():
    screen = pg.display.set_mode((1280, 720))
    clock = pg.time.Clock()
    maze = pg.sprite.Group()

    maze_matrix = []
    for i in range(MAZE_MAX):
        maze_row = []
        for j in range(MAZE_MAX):
            point = Point(i, j)
            maze.add(point)
            maze_row.append(point)
        maze_matrix.append(maze_row)

    done = False
    x = np.zeros(50)
    y = np.zeros(50)
    i = 0

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        if i <= 20:
            i = randomwalk2D(50, x, y, i, MAZE_MAX)
            print(x)
        if i == 20:
            print(x)
            print(y)
            i += 1
            for j in range(20):
                maze_matrix[int(x[j])][int(y[j])].change_color()

        maze.update()
        screen.fill(BLACK)
        pg.draw.rect(screen, (100, 100, 100), (LEFT-POINT_SIZE, TOP-POINT_SIZE,
                     POINT_SIZE*(2+MAZE_MAX), POINT_SIZE*(2+MAZE_MAX)))
        maze.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
