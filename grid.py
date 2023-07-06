from pygame import draw
import numpy as np


class Grid:
    def __init__(
        self,
        screen,
        n_cellx,
        n_celly,
        wall_thick,
    ):
        self.screen = screen
        self.n_cellx = n_cellx
        self.n_celly = n_celly
        self.wall_thick = wall_thick
        self.cell_state = np.zeros((n_cellx, n_celly), dtype=int)
        self.wall_state = np.zeros((n_cellx, n_celly, 2), dtype=int)
        self.width_cell = (screen.get_width() - (n_cellx - 1) * wall_thick) / n_cellx
        self.height_cell = (screen.get_height() - (n_celly - 1) * wall_thick) / n_celly

    def color_cell(self, x1, x2, color):
        self.cell_state[x1][x2] = color

    def color_wall(self, x1, x2, z, color):
        self.wall_state[x1][x2][z] = color

    def color_path(self, previous, to, color):
        if previous[0] == to[0]:  # vertical move
            if previous[1] > to[1]:  # up move
                self.color_wall(to[0], to[1], 1, color)
            else:  # down move
                self.color_wall(previous[0], previous[1], 1, color)

        elif previous[1] == to[1]:  # horizontal move
            if previous[0] > to[0]:  # left move
                self.color_wall(to[0], to[1], 0, color)
            else:  # right move
                self.color_wall(previous[0], previous[1], 0, color)

        else: 
            raise ValueError("Diagonal moves are not posible")

        self.color_cell(to[0], to[1], color)

    def draw(self):
        screen = self.screen
        n_cellx = self.n_cellx
        n_celly = self.n_celly
        wall_thick = self.wall_thick
        cell_state = self.cell_state
        wall_state = self.wall_state
        width_cell = self.width_cell
        height_cell = self.height_cell

        for y in range(n_cellx):
            for x in range(n_celly):
                cell = [
                    (x * (width_cell + wall_thick), y * (height_cell + wall_thick)),
                    (
                        x * (width_cell + wall_thick) + width_cell,
                        y * (height_cell + wall_thick),
                    ),
                    (
                        x * (width_cell + wall_thick) + width_cell,
                        y * (height_cell + wall_thick) + height_cell,
                    ),
                    (
                        x * (width_cell + wall_thick),
                        y * (height_cell + wall_thick) + height_cell,
                    ),
                ]

                if cell_state[x][y] == 1:
                    draw.polygon(screen, (255, 255, 255), cell)
                elif cell_state[x][y] == 2:
                    draw.polygon(screen, (255, 0, 0), cell)
                else:
                    draw.polygon(screen, (0, 0, 0), cell)

                # walls
                if (
                    x != n_cellx - 1 or y != n_celly - 1
                ):  # last iteration draws no walls
                    wall_v = [  # vertical
                        (
                            x * (width_cell + wall_thick) + width_cell,
                            y * (height_cell + wall_thick),
                        ),
                        (
                            (x + 1) * (width_cell + wall_thick),
                            y * (height_cell + wall_thick),
                        ),
                        (
                            (x + 1) * (width_cell + wall_thick),
                            (y + 1) * (height_cell + wall_thick),
                        ),
                        (
                            x * (width_cell + wall_thick) + width_cell,
                            (y + 1) * (height_cell + wall_thick),
                        ),
                    ]

                    wall_h = [  # horizontal
                        (
                            x * (width_cell + wall_thick),
                            y * (height_cell + wall_thick) + height_cell,
                        ),
                        (
                            (x + 1) * (width_cell + wall_thick),
                            y * (height_cell + wall_thick) + height_cell,
                        ),
                        (
                            (x + 1) * (width_cell + wall_thick),
                            (y + 1) * (height_cell + wall_thick),
                        ),
                        (
                            x * (width_cell + wall_thick),
                            (y + 1) * (height_cell + wall_thick),
                        ),
                    ]

                    if wall_state[x][y][0] == 1:
                        draw.polygon(screen, (255, 255, 255), wall_v)
                    elif wall_state[x][y][0] == 2:
                        draw.polygon(screen, (255, 0, 0), wall_v)
                    else:
                        draw.polygon(screen, (0, 0, 0), wall_v)

                    if wall_state[x][y][1] == 1:
                        draw.polygon(screen, (255, 255, 255), wall_h)
                    elif wall_state[x][y][1] == 2:
                        draw.polygon(screen, (255, 0, 0), wall_h)
                    else:
                        draw.polygon(screen, (0, 0, 0), wall_h)

                    if wall_state[x][y][1] and not wall_state[x][y][0]:
                        draw.polygon(screen, (0, 0, 0), wall_v)
