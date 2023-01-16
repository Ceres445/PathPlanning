import unittest
from maze import Maze
from rrt import convert_maze


class NodeGraph:
    def __init__(self, maze) -> None:
        self.nodes = []
        self.edges = []
        self.maze = maze
        self.node_dict = {}

        self.valid_points = [
            (j, i)
            for i in range(len(maze))
            for j in range(len(maze[0]))
            if maze[i][j] == 1
        ]

    @classmethod
    def from_maze(cls, maze, nodes, edges):
        graph = cls(maze)
        for node in nodes:
            graph.nodes.append(node)

        for edge in edges:
            graph.edges.append(edge)
        return graph

    def add_node_edge(self, node1, node2):
        self.edges.append((node1, node2))
        if self.node_dict.get(node1) is None:
            self.node_dict[node1] = [node2]
        else:
            self.node_dict[node1].append(node2)

        if self.node_dict.get(node2) is None:
            self.node_dict[node2] = [node1]
        else:
            self.node_dict[node2].append(node1)

    def add_edge(self, direction, node):
        x, y = node
        # print("trying to add edge", direction, node)
        if direction == "up":
            # line = [arr[x] for arr in self.maze[:y]]
            # try:
            #     wall = y - line[::-1].index(0)
            # except ValueError:
            #     wall = 0

            node = [node for node in self.nodes if node[0] == x]
            # self.add_node_edge((x, wall), node)

            self.add_node_edge(max(node, key=lambda x: x[1]), (x, y))

        elif direction == "left":
            # line = self.maze[y][:x]
            # try:
            #     wall = x - line[::-1].index(0)
            # except ValueError:
            #     wall = 0
            # self.add_node_edge((wall, y), node)
            node = [node for node in self.nodes if node[1] == y]
            self.add_node_edge(max(node, key=lambda x: x[0]), (x, y))

    def get_edges(self, node):
        edges = []
        for edge in self.edges:
            if edges == 4:
                break
            if edge[0] == node:
                edges.append(edge)
            elif edge[1] == node:
                edges.append(edge)
        return edges

    def plot(self, node_color="red", edge_color="blue"):
        import matplotlib.pyplot as plt
        from matplotlib import axes

        _, ax = plt.subplots()

        # type hint for lsp
        ax: axes.Axes = ax
        # ax.pcolormesh(maze, cmap="gray")
        walls = convert_maze(self.maze)
        for wall in walls:
            ax.plot(*zip(*wall), color="black")
        for node in self.nodes:
            ax.scatter(*node, color=node_color)

        for edge in self.edges:
            ax.plot(*zip(*edge), color=edge_color)
        # for node in self.valid_points:
        #     ax.scatter(*node, color="blue")
        # plt.pcolormesh(maze)
        ax.set_aspect("equal")
        # plt.axes().set_aspect("equal")  # set the x and y axes to the same scale
        # plt.xticks([])
        # plt.yticks([])
        ax.invert_yaxis()
        plt.show()


def find_directions(maze, x, y):
    directions = []
    if x > 0 and maze[y][x - 1] == 1:
        directions.append("left")
    if (x < len(maze[y]) - 1) and maze[y][x + 1] == 1:
        directions.append("right")
    if y > 0 and maze[y - 1][x] == 1:
        directions.append("up")
    if y < len(maze) - 1 and maze[y + 1][x] == 1:
        directions.append("down")
    return directions


def generate_nodes(maze: Maze) -> NodeGraph:
    """Generate a graph of nodes and edges from a maze.

    Args:
        maze (Maze): The maze to generate the graph from.

    Returns:
        NodeGraph: The graph of nodes and edges.
    """

    graph = NodeGraph(maze.get_maze_array())
    maze_array = maze.get_maze_array()

    for j in range(len(maze_array)):
        for i in range(len(maze_array[j])):
            if maze_array[j][i] == 1:
                directions = find_directions(maze_array, i, j)
                if len(directions) != 2 or set(directions) not in [
                    {"up", "down"},
                    {"left", "right"},
                ]:
                    for direction in directions:
                        if direction in ("up", "left"):
                            graph.add_edge(direction, (i, j))

                    graph.nodes.append((i, j))
    return graph


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

        class TestMaze(Maze):
            def __init__(self):
                self.entrance = (1, 1)
                self.exit = (19, 19)
                self.maze = maze_array

            def get_maze_array(self):
                return maze_array

        graph = generate_nodes(TestMaze())
        # graph.plot()
        self.assertEqual(len(graph.nodes), 73)
        self.assertEqual(len(graph.valid_points), 201)
        for cur, val in graph.node_dict.items():
            for node in val:
                print(node, cur, graph.node_dict[node])
                assert node in graph.nodes
                assert cur in graph.node_dict[node]



if __name__ == "__main__":
    TestGraph().test_graph()
    # maze = Maze(20, 20)
    # graph = generate_nodes(maze)
    # graph.plot()
