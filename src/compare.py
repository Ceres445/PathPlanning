from helpers.maze import Maze 
from rrt import run_rrt
from djikstra import run_djikstra


if __name__ == "__main__":
    maze = Maze(5, 5)

    print("------------")
    print("Size: 5")
    run_rrt(maze)
    run_djikstra(maze)


    maze = Maze(10, 10)
    print("------------")
    print("Size: 10")
    # run_rrt(maze)
    run_djikstra(maze)

    maze = Maze(20, 20)
    print("------------")
    print("Size: 20")
    # run_rrt(maze)
    run_djikstra(maze)

    maze = Maze(50, 50)
    print("------------")
    print("Size: 50")
    run_djikstra(maze)

    maze = Maze(100, 100)
    print("------------")
    print("Size: 100")
    run_djikstra(maze)
