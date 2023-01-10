import maze
from shapely import linestrings
from rrt import convert_maze
from shapely.geometry import Polygon

import numpy as np
from matplotlib.path import Path
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.collections import PatchCollection


# Plots a Polygon to pyplot `ax`
def plot_polygon(ax, poly, **kwargs):
    path = Path.make_compound_path(
        Path(np.asarray(poly.exterior.coords)[:, :2]),
        *[Path(np.asarray(ring.coords)[:, :2]) for ring in poly.interiors]
    )

    patch = PathPatch(path, **kwargs)
    collection = PatchCollection([patch], **kwargs)

    ax.add_collection(collection, autolim=True)
    ax.autoscale_view()
    return collection


def plot_lines(ax, lines, **kwargs):
    for line in lines:
        ax.plot(*line.xy, **kwargs)

    ax.set_aspect("equal")
    ax.set_xticks([], "")
    ax.set_yticks([], "")
    ax.invert_yaxis()


if __name__ == "__main__":
    maze = maze.Maze(20, 20)

    maze_array = maze.get_maze_array()

    print(list(convert_maze(maze_array)))
    # print each line seperately
    print(*list(maze.get_maze_array()), sep="\n")
    print(maze)
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # fig, ax = plt.subplots()

    maze_object = linestrings(list(convert_maze(maze_array)))
    plot_lines(ax1, maze_object, color="black")
    maze.plot(ax2)
    # maze_object = Polygon(convert_maze(maze_array))
    # plot_polygon(ax, maze_object, facecolor="lightblue", edgecolor="black")
    plt.show()
