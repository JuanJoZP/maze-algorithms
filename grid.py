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
        self.cell_state = np.zeros((n_cellx, n_celly), dtype=bool)
        self.wall_state = np.zeros((n_cellx, n_celly, 2), dtype=bool)
        self.width_cell = (screen.get_width() - (n_cellx - 1) * wall_thick) / n_cellx
        self.height_cell = (screen.get_height() - (n_celly - 1) * wall_thick) / n_celly

    def activate_cell(self, y, x):
        self.cell_state[x][y] = 1

    def activate_wall(self, y, x, z):
        self.wall_state[x][y][z] = 1

    def deactivate_cell(self, y, x):
        self.cell_state[x][y] = 0

    def deactivate_wall(self, y, x, z):
        self.wall_state[x][y][z] = 0

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
                # celdas
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

                if cell_state[x][y]:
                    draw.polygon(screen, (255, 255, 255), cell)
                else:
                    draw.polygon(screen, (0, 0, 0), cell)

                # paredes
                if (
                    x != n_cellx - 1 or y != n_celly - 1
                ):  # La ultima iteracion no dibuja paredes
                    wall_v = [  # pared vertical
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

                    wall_h = [  # pared horizontal
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

                    if wall_state[x][y][0]:
                        draw.polygon(screen, (255, 255, 255), wall_v)
                    else:
                        draw.polygon(screen, (0, 0, 0), wall_v)

                    if wall_state[x][y][1]:
                        draw.polygon(screen, (255, 255, 255), wall_h)
                    else:
                        draw.polygon(screen, (0, 0, 0), wall_h)

                    if wall_state[x][y][1] and not wall_state[x][y][0]:
                        draw.polygon(screen, (0, 0, 0), wall_v)
