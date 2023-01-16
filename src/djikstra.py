from helpers.generate_nodes import NodeGraph, generate_nodes, unittest
from helpers.maze import Maze


def min_val(di):
    return min(di, key=lambda x: di.get(x)[0])


def djikstra(graph: NodeGraph, start: tuple, end: tuple) -> list:
    current = start
    finished = [start]
    edges = {x: [1, current] for x in graph.node_dict[current]}
    current = min_val(edges)
    old = {start: [0, None]}
    while current != end:
        for edge in graph.node_dict[current]:
            if edge not in finished:
                if edge not in edges:
                    edges[edge] = [edges[current][0] + 1, current]
                else:
                    edges[edge] = min(
                        edges[edge],
                        [edges[current][0] + 1, current],
                        key=lambda x: x[0],
                    )

        finished.append(current)
        old[current] = edges.pop(current)
        # print(finished)
        # print(edges)
        current = min_val(edges)

    old[current] = edges.pop(current)
    nodes = [end]
    edges = []
    while nodes[-1] != start:
        nodes.append(old[nodes[-1]][1])
        edges.append((nodes[-1], nodes[-2]))

    return [nodes, edges]


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
                self.entrance = (1, 0)
                self.exit = (17, 20)
                self.maze = maze_array

            def get_maze_array(self):
                return maze_array

        graph = generate_nodes(TestMaze())
        # print(graph.nodes)
        # print(graph.node_dict)
        # from matplotlib import pyplot as plt
        # _, ax = plt.subplots()
        # graph.plot(ax)
        nodes, edges = djikstra(graph, (0, 1), (20, 17))
        grpah = NodeGraph.from_maze(TestMaze().maze, nodes, edges)
        grpah.plot()

        self.assertEqual(len(graph.nodes), 73)
        self.assertEqual(len(graph.valid_points), 201)


def run_djikstra(maze, plot=False):
    print("------------")
    print("Djikstra")
    import time

    a = time.perf_counter()
    print(f"Size of maze: ( nxn )", len(maze.get_maze_array()))
    graph = generate_nodes(maze)
    print(f"Generating nodes took {time.perf_counter() - a} seconds")
    print("Nodes:", len(graph.nodes))
    print("Valid points:", len(graph.valid_points))
    a = time.perf_counter()
    nodes, edges = djikstra(graph, (0, maze.entrance), (maze.ny * 2, maze.exit))
    if plot:
        NodeGraph.from_maze(maze.get_maze_array(), nodes, edges).plot()
    print(f"Finding path took {time.perf_counter() - a} seconds")
    print("Nodes:", len(nodes))
    print("Edges:", len(edges))
    # grpah = NodeGraph.from_maze(maze.get_maze_array(), nodes, edges)
    # grpah.plot()
    # TestGraph().test_graph()


if __name__ == "__main__":
    n = int(input("Enter the size of the maze: "))
    run_djikstra(Maze(n, n), plot=True)
    # run(10)
    # run(100)
    # run(200)
