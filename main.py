from cgi import print_form
import pygame as pg

BLACK = pg.Color(0, 0, 0)
WHITE = pg.Color(255, 255, 255)
POINT_SIZE = 15
TOP = 200
LEFT = 250
MAZE_X = 50
MAZE_Y = 20


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
    for i in range(MAZE_X):
        maze_row = []
        for j in range(MAZE_Y):
            point = Point(i, j)
            maze.add(point)
            maze_row.append(point)
            maze_matrix.append(maze_row)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        maze.update()
        screen.fill(BLACK)
        pg.draw.rect(screen, (100, 100, 100), (LEFT-POINT_SIZE, TOP-POINT_SIZE,
                     POINT_SIZE*(2+MAZE_X), POINT_SIZE*(2+MAZE_Y)))
        maze.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
