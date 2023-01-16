import random
import unittest
from shapely import LineString, Point, linestrings
from helpers.maze import Maze, plt
from helpers.generate_nodes import convert_maze


class Graph:
    def __init__(self, maze, entrance, goal) -> None:
        self.nodes = [Point(0, entrance)]
        self.edges = []
        self.maze = maze
        self.goal = goal

    def nearest_node(self, point: Point):
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
            if self.validline(line) and line.length == 1 and is_orthogonal(line):
                if current is None:
                    current = line
                else:
                    if line.length < current.length:
                        current = line
        if current is None:
            return None
        else:
            return current

    def find_path(self, ax, goal=None, edges=[], nodes=[], old=[], plot=False):
        current = goal or self.goal
        color = "blue"
        if current == self.nodes[0]:
            color = "yellow"
        state = 0

        for edge in self.edges:
            if current.coords[0] in edge.coords and edge not in edges:
                state = 1
                edges.append(edge)
                if edge.coords[0] == current.coords[0]:
                    nodes.append(Point(edge.coords[1]))
                else:
                    nodes.append(Point(edge.coords[0]))

        if plot:
            ax.plot(*current.xy, marker="o", color="red")
            for edge in edges:
                ax.plot(*edge.xy, color="red")

            for node in nodes:
                ax.plot(*node.xy, marker="o", color=color)

            for node in old:
                ax.plot(*node.xy, marker="o", color="green")

            for line in self.maze:
                ax.plot(*line.xy, color="white")
            plt.pause(0.01)
        if color == "yellow":
            return nodes, edges

        if not state:
            if len(nodes) > 1:
                # print("popping")
                old.append(nodes.pop())
                return self.find_path(
                    goal=nodes[-1], edges=edges, nodes=nodes, ax=ax, old=old, plot=plot
                )
            return print("UNABLE TO FIND PATH", edges, goal, current, self.nodes)

        return self.find_path(goal=nodes[-1], edges=edges, nodes=nodes, ax=ax, old=old, plot=plot)

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
            ax.plot(*line.xy, color="white")

        for node in self.nodes:
            ax.plot(*node.xy, marker="o", color="blue")

        ax.plot(*self.goal.xy, marker="o", color="green")


def is_orthogonal(line: LineString):
    return (
        line.coords[0][0] == line.coords[1][0] or line.coords[0][1] == line.coords[1][1]
    )


def rrt(maze: Maze, plot: bool = False):
    # goal point is one point left to the last position

    lim = 1000
    maze_array = maze.get_maze_array()
    # print(maze_array)
    qgoal = Point(len(maze_array) - 1, maze.exit)

    maze_object = linestrings(list(convert_maze(maze_array)))
    # print(maze_object)

    graph = Graph(maze_object, maze.entrance, qgoal)


    fig, ax1, ax2 = [None, None, None] # fool lsp
    if plot:
        # get two subplots
        fig, [ax1, ax2] = plt.subplots(1, 2, figsize=(10, 5))

        fig.patch.set_facecolor('black')

        ax1.set_facecolor('black')
        ax1.set_aspect("equal")
        ax1.set_xticks([], "")
        ax1.set_yticks([], "")
        ax2.set_aspect("equal")
        ax2.set_facecolor('black')
        ax2.set_xticks([], "")
        ax2.set_yticks([], "")
        ax1.invert_yaxis()
        ax2.invert_yaxis()

    valid_points = [
        (j, i)
        for i in range(len(maze_array))
        for j in range(len(maze_array[0]))
        if maze_array[i][j] == 1
    ]
    while lim > 0:
        # node = random.choice(graph.nodes)
        # qrand = random.choice([(node.x +1, node.y), (abs(node.x - 1), node.y), (node.x, node.y + 1), (node.x, abs(node.y - 1))])
        qrand = random.choice(valid_points)

        # qrand = [
        #     (
        #         random.choice([x.x for x in graph.nodes]),
        #         random.randint(0, len(maze_array)),
        #     ),
        #     (
        #         random.randint(0, len(maze_array) - 1),
        #         random.choice([y.y for y in graph.nodes]),
        #     ),
        # ][random.randint(0, 1)]

        qnear = graph.nearest_node(Point(qrand))

        # print(f"Valid points: {len(valid_points)}")
        if qnear is not None:
            lim -= 1
            if graph.validline(LineString([qrand, qgoal])):
                graph.nodes.append(Point(qrand))
                graph.edges.append(qnear)
                graph.nodes.append(Point(qgoal))
                graph.edges.append(LineString([qrand, qgoal]))
                if plot:
                    graph.plot(ax1)
                    plt.pause(0.01)
                # print("BREAK")
                break
            if qrand in valid_points:
                valid_points.remove(qrand)
            graph.nodes.append(Point(qrand))
            graph.edges.append(qnear)
            if plot:
                graph.plot(ax1)
                plt.pause(0.01)
    # print(graph.nodes)

    graph.find_path(ax=ax2, plot=plot)

    plt.show()




def run_rrt(maze):
    print("------------")
    print("RRT")
    import time

    a = time.perf_counter()
    rrt(maze)
    print("Time taken: ", time.perf_counter() - a)


if __name__ == "__main__":
    n = int(input("Enter size of nxn maze"))
    rrt(Maze(n, n), plot=True)

    # rrt(Maze(10, 10))


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
        self.assertEqual(graph.nearest_node(Point(1, 0)), LineString([(0, 1), (0, 2)]))
