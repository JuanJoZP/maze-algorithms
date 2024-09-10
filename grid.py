from pygame import draw
import numpy as np
import math


# class managing the grid rendering and the player movement
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

        self.player_pos = [0, 0]
        self.player_queue = []

    # returns the window coordinates resulting of moving from 'start' in 'direction'
    def get_end(self, start, direction, move=None):
        if move == None:
            move = self.width_cell + self.wall_thick

        if direction == "up":
            return (start[0], start[1] - move)
        if direction == "down":
            return (start[0], start[1] + move)
        if direction == "left":
            return (start[0] - move, start[1])
        if direction == "right":
            return (start[0] + move, start[1])

    # returns true if dir1 is the opposite direction of dir2
    def is_inverse(self, dir1, dir2):
        if dir2 is None:
            return False

        if dir1 == "up" and dir2 == "down":
            return True
        if dir2 == "up" and dir1 == "down":
            return True
        if dir1 == "left" and dir2 == "right":
            return True
        if dir2 == "left" and dir1 == "right":
            return True

        return False

    def move_player(self, direction):
        player_queue = self.player_queue
        player_pos = self.player_pos

        move = self.get_end(self.player_pos, direction, 1)

        # wont move if the movement is out of bounds
        if np.any((np.asarray(move) < 0) | (np.asarray(move) >= self.n_cellx)):
            return

        # wont move if the movement meets a wall
        if direction == "up" or direction == "down":
            if self.wall_state[player_pos[0]][min(move[1], player_pos[1])][1] == 0:
                return
        if direction == "left" or direction == "right":
            if self.wall_state[min(move[0], player_pos[0])][player_pos[1]][0] == 0:
                return

        # move
        self.player_pos = move

        if self.is_inverse(direction, player_queue[-1] if len(player_queue) != 0 else None):
            player_queue.pop()
        else:
            player_queue.append(direction)

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
        player_queue = self.player_queue

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

                if cell_state[x][y] == 1:  # white cells (corridors)
                    draw.polygon(screen, (255, 255, 255), cell)
                elif cell_state[x][y] == 2:  # red cells (cells in generation process)
                    draw.polygon(screen, (255, 0, 0), cell)
                elif cell_state[x][y] == 3:  # white cell with a red circle (start and end)
                    draw.polygon(screen, (255, 255, 255), cell)
                    draw.circle(
                        screen,
                        (255, 0, 0),
                        (
                            x * (width_cell + wall_thick) + width_cell / 2,
                            y * (height_cell + wall_thick) + height_cell / 2,
                        ),
                        width_cell * 0.3,
                    )
                else:
                    draw.polygon(screen, (0, 0, 0), cell)

                # walls
                if x != n_cellx - 1 or y != n_celly - 1:  # last iteration draws no walls
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

                # draws player
                start = (width_cell / 2, width_cell / 2)
                for direction in player_queue:
                    end = self.get_end(start, direction)
                    draw.line(
                        screen, (255, 0, 0), start, end, math.ceil(self.n_cellx / 5)
                    )  # red line
                    start = end
