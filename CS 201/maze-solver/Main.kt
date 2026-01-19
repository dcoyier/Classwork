// Author: Dashiell Coyier
// Source code from Carleton College CS 201 f25, taught by Anya Vostinar


fun main(args: Array<String>) {
    if (args.size == 2 && args[1] == "--solve") {
        var myMaze = SolvableMaze(args[0])
        myMaze.solveMaze()
        myMaze.printMaze()
    } else if (args.size == 1) {
        var myMaze = Maze(args[0])
        myMaze.printMaze()
    } else {
        // assume top maze wants to be solved
        var myMaze = SolvableMaze("maze.txt")
        myMaze.solveMaze()
        myMaze.printMaze()
    }
}
