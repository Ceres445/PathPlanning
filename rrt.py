import random
import unittest
from shapely import LineString, Point, linestrings
from maze import Maze, plt


class Graph:
    def __init__(self, maze, entrance, goal) -> None:
        self.nodes = [Point(0, entrance)]
        self.edges = []
        self.maze = maze
        self.goal = goal

    def nearest(self, point: Point):
        current = None
        if point in self.nodes:
            return None
        for edge in self.edges:
            if edge.contains(point):
                return None
        for wall in self.maze:
            if wall.contains(point):
                return None
        for node in self.nodes:
            line = LineString([point, node])
            if (
                self.validline(line)
                # and line.length == 1
                # and is_orthogonal(line)
            ):
                if current is None:
                    current = line
                else:
                    if line.length < current.length:
                        current = line
        if current is None:
            return None
        else:
            return current

    def find_path(self, goal=None, edges=[], nodes=[], ax = None, old = []):

        if ax is None:
            _, ax = plt.subplots()
            ax: plt.Axes

        current = goal or self.goal
        color = 'blue'
        if current == self.nodes[0]:
            color = 'yellow'
        state = 0

        for edge in self.edges:
            if current.coords[0] in edge.coords and edge not in edges:
                state = 1
                edges.append(edge)
                if edge.coords[0] == current.coords[0]:
                    nodes.append(Point(edge.coords[1]))
                else:
                    nodes.append(Point(edge.coords[0]))
        
        ax.plot(*current.xy, marker="o", color="red")
        for edge in edges:
            ax.plot(*edge.xy, color="red")


        for node in nodes:
            ax.plot(*node.xy, marker="o", color=color)

        for node in old:
            ax.plot(*node.xy, marker="o", color="green")

        for line in self.maze:
            ax.plot(*line.xy, color="black")
        plt.pause(0.01)
        if color == 'yellow':
            return nodes, edges

        if not state:
            if len(nodes) > 1:
                print('popping')
                old.append(nodes.pop())
                return self.find_path(goal=nodes[-1], edges=edges, nodes=nodes, ax=ax, old = old)
            return print("UNABLE TO FIND PATH", edges, goal, current, self.nodes)

        print(nodes)
        return self.find_path(goal=nodes[-1], edges=edges, nodes=nodes, ax=ax, old = old)



    def validline(self, line: LineString) -> bool:
        for edge in self.edges:
            if edge.contains(line):
                return False
        for wall in self.maze:
            if line.coords[1] in wall.coords:
                continue
            if line.intersects(wall):
                # print(f"{line} intersects {wall} at {line.intersection(wall)}")
                return False
        return True

    def plot(self, ax):
        for edge in self.edges:
            ax.plot(*edge.xy, color="red")

        for line in self.maze:
            ax.plot(*line.xy, color="black")

        for node in self.nodes:
            ax.plot(*node.xy, marker="o", color="blue")

        ax.plot(*self.goal.xy, marker="o", color="green")


def is_orthogonal(line: LineString):
    return (
        line.coords[0][0] == line.coords[1][0] or line.coords[0][1] == line.coords[1][1]
    )


def rrt(maze: Maze):
    # goal point is one point left to the last position

    lim = 1000
    maze_array = maze.get_maze_array()
    # print(maze_array)
    qgoal = Point(len(maze_array) - 1, maze.exit)

    maze_object = linestrings(list(convert_maze(maze_array)))
    # print(maze_object)

    graph = Graph(maze_object, maze.entrance, qgoal)
    
    # get two subplots
    _, [ax1, ax2] = plt.subplots(1, 2, figsize=(10, 5))

    ax1.set_aspect("equal")
    ax1.set_xticks([], "")
    ax1.set_yticks([], "")
    ax2.set_aspect("equal")
    ax2.set_xticks([], "")
    ax2.set_yticks([], "")
    ax1.invert_yaxis()
    ax2.invert_yaxis()
    while lim > 0:
        # node = random.choice(graph.nodes)
        # qrand = random.choice([(node.x +1, node.y), (abs(node.x - 1), node.y), (node.x, node.y + 1), (node.x, abs(node.y - 1))])
        qrand = [
            (
                random.choice([x.x for x in graph.nodes]),
                random.randint(0, len(maze_array)),
            ),
            (
                random.randint(0, len(maze_array) - 1),
                random.choice([y.y for y in graph.nodes]),
            ),
        ][random.randint(0, 1)]

        qnear = graph.nearest(Point(qrand))
        if qnear is not None:
            lim -= 1
            if graph.validline(LineString([qrand, qgoal])):
                graph.nodes.append(Point(qrand))
                graph.edges.append(qnear)
                graph.nodes.append(Point(qgoal))
                graph.edges.append(LineString([qrand, qgoal]))
                graph.plot(ax1)
                plt.pause(0.01)
                print("BREAK")
                break
            graph.nodes.append(Point(qrand))
            graph.edges.append(qnear)
            graph.plot(ax1)
            plt.pause(0.01)
    print(graph.nodes)

    graph.find_path(ax=ax2)

    plt.show()


def convert_maze(maze_array):
    # convert maze array to shapely polygon
    # [[0, 0, 0, 0, 1],
    #  [1, 1, 1, 1, 0],
    #  [0, 0, 0, 1, 0],
    #  [0, 1, 1, 1, 0],
    #  [0, 0, 0, 0, 0]]

    # to
    # [(1,0), (1,1), (1,2), (1,3), (1,4), (2,4), (3,4), (4,4), (4,3), (4,2), (4,1), (4,0), (3,0), (2,0), (1,0)]

    for j in range(len(maze_array)):
        state = 0
        start = 0
        end = 0
        for i in range(len(maze_array[j])):
            if maze_array[j][i] == 0:
                if state == 0:
                    state = 1
                    start = i
                    end = i
                else:
                    end = i
            else:
                if state == 1:
                    state = 0
                    if start != end:
                        yield [[start, j], [end, j]]
        if state == 1 and start != end:
            yield [[start, j], [end, j]]

    for i in range(len(maze_array[0])):
        state = 0
        start = 0
        end = 0
        for j in range(len(maze_array)):
            if maze_array[j][i] == 0:
                if state == 0:
                    state = 1
                    start = j
                    end = j
                else:
                    end = j
            else:
                if state == 1:
                    state = 0
                    if start != end:
                        yield [[i, start], [i, end]]
        if state == 1 and start != end:
            yield [[i, start], [i, end]]


if __name__ == "__main__":
    rrt(Maze(10, 10))
    # rrt(Maze(5, 5))


class TestGraph(unittest.TestCase):
    def test_graph(self):
        maze_array = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        maze_object = linestrings(list(convert_maze(maze_array)))
        graph = Graph(maze_object, 1, Point([17, 20]))
        self.assertEqual(graph.nearest(Point(1, 0)), LineString([(0, 1), (0, 2)]))
