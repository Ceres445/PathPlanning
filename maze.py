import random
from matplotlib.projections import axes
import matplotlib.pyplot as plt
import matplotlib


class Cell:
    wall_pairs = {"Up": "Down", "Down": "Up", "Right": "Left", "Left": "Right"}

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"Up": True, "Down": True, "Right": True, "Left": True}


class Maze:
    def __init__(self, nx, ny):
        self.nx, self.ny = nx, ny
        self.maze_map = [[Cell(x, y) for y in range(ny)] for x in range(nx)]
        self.entrance = 0
        self.exit = 0
        self._make_maze()

    def get_maze_array(self):
        maze = [[0 for _ in range(self.nx * 2 + 1)]]
        for y in range(self.ny):
            row1 = [0]  # start each row with a wall
            row2 = [0]
            for x in range(self.nx):
                if not self.maze_map[x][y].walls["Right"]:
                    row1.append(1)  # spaces are ones and walls are zeros
                    row1.append(1)
                else:
                    row1.append(1)
                    row1.append(0)
                if self.maze_map[x][y].walls["Down"]:
                    row2.append(0)
                    row2.append(0)
                else:
                    row2.append(1)
                    row2.append(0)
            maze.append(row1)
            maze.append(row2)
        maze[self.entrance][0] = 1  # open entrance and exit
        maze[self.exit][-1] = 1
        return maze

    def plot(self, ax=None):
        maze = self.get_maze_array()
        if ax is None:
            _, ax = plt.subplots()

        # type hint for lsp
        ax: axes.Axes = ax
        ax.pcolormesh(maze, cmap="gray")
        # plt.pcolormesh(maze)
        ax.set_aspect("equal")
        # plt.axes().set_aspect("equal")  # set the x and y axes to the same scale
        plt.xticks([])  # remove the tick marks by setting to an empty list
        plt.yticks([])  # remove the tick marks by setting to an empty list
        # plt.axes().invert_yaxis()  # invert the y-axis so the first row of data is at the top
        # plt.savefig("tet.png")
        ax.invert_yaxis()

        plt.show()

    def _find_neighbours(self, cell):
        directions = [
            ("Left", (-1, 0)),
            ("Right", (1, 0)),
            ("Down", (0, 1)),
            ("Up", (0, -1)),
        ]
        neighbours = []
        for direction, (dx, dy) in directions:
            x2, y2 = cell.x + dx, cell.y + dy
            if (0 <= x2 < self.nx) and (0 <= y2 < self.ny):
                neighbour = self.maze_map[x2][y2]
                if all(neighbour.walls.values()): # if neighbour has all walls
                    neighbours.append((direction, neighbour))
        return neighbours

    def _make_maze(self):
        n = self.nx * self.ny
        cells = []
        current = self.maze_map[0][0]
        nv = 1

        while nv < n:
            neighbours = self._find_neighbours(current)

            if not neighbours:
                current = cells.pop()
                continue
            direction, next_cell = random.choice(neighbours)

            current.walls[direction] = False
            next_cell.walls[Cell.wall_pairs[direction]] = False
            cells.append(current)
            current = next_cell
            nv += 1

        for y in range(self.ny):
            if self.maze_map[y][0].walls["Right"] or self.maze_map[y][0].walls["Down"]:
                self.entrance = y * 2 + 1
                break

        for y in range(self.ny - 1, 0, -1):
            if self.maze_map[y][-1].walls["Left"] or self.maze_map[y][-1].walls["Up"]:
                self.exit = y * 2 + 1
                break
