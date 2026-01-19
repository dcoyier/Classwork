// class representing a maze that can be solved
class SolvableMaze(filename: String): Maze(filename) {
    // initializing the stack to hold the solution path
    val solution = ListStack<MazeSquare>()

    /*
    The function solveMaze() takes no parameters and updates a maze with its solution
    @return true or false whether the maze can be solved
    */
    fun solveMaze(): Boolean {
        solution.push(squares[startRow][startCol])
        squares[startRow][startCol].visited = true

        while (!solution.isEmpty()) {
            // topSquare is the square on top of the stack
            var topSquare = solution.peek()

            // checking if topSquare is the finish square; if so, the squares in the solution stack are marked as solution pieces
            if (topSquare == squares[finishRow][finishCol]) {
                while (!solution.isEmpty()) {
                    solution.pop().solutionPiece = true
                }

                return true
            }

            // if not the finish square, determine what the next square will be
            if (checkAndAddTop(topSquare)) {
                continue
            } else if (checkAndAddRight(topSquare)) {
                continue
            } else if (checkAndAddLeft(topSquare)) {
                continue
            } else if (checkAndAddDown(topSquare)) {
                continue
            } else {
                solution.pop()
            }
        }

        // return false if no open square was found adjacent to the square atop the stack
        return false
    }

    /*
    The function checkTop() determines if the square below is available. If so, it adds it to the solution stack
    @param the square on top of the solution stack
    @return true or false, dependent on if the square below was open, available, and if it was added to the solution stack
    */
    fun checkAndAddTop(topSquare: MazeSquare): Boolean {
        if (topSquare.row != 0 && topSquare.hasTopWall != true && squares[topSquare.row - 1][topSquare.col].visited == false) {
            solution.push(squares[topSquare.row - 1][topSquare.col])
            solution.peek().visited = true
            return true
        }
        return false
    }

    /*
    The function checkRight() determines if the square to the right is available. If so, it adds it to the solution stack
    @param the square on top of the solution stack
    @return true or false, dependent on if the square to the right was open, available, and if it was added to the solution stack
    */
    fun checkAndAddRight(topSquare: MazeSquare): Boolean {
        if (topSquare.col != numCols && topSquare.hasRightWall != true && squares[topSquare.row][topSquare.col + 1].visited == false) {
            solution.push(squares[topSquare.row][topSquare.col + 1])
            solution.peek().visited = true
            return true
        }
        return false
    }
    /*
    The function checkLeft() determines if the square to the left is available. If so, it adds it to the solution stack
    @param the square on top of the solution stack
    @return true or false, dependent on if the square to the left was open, available, and if it was added to the solution stack
    */
    fun checkAndAddLeft(topSquare: MazeSquare): Boolean {
        if (topSquare.col != 0 && squares[topSquare.row][topSquare.col - 1].hasRightWall != true && squares[topSquare.row][topSquare.col - 1].visited == false) {
            solution.push(squares[topSquare.row][topSquare.col - 1])
            solution.peek().visited = true
            return true
        }
        return false
    }

    /*
    The function checkDown() determines if the square above is available. If so, it adds it to the solution stack
    @param the square on top of the solution stack
    @return true or false, dependent on if the square above was open, available, and if it was added to the solution stack
    */
    fun checkAndAddDown(topSquare: MazeSquare): Boolean {
        if (topSquare.row != numRows - 1 && squares[topSquare.row + 1][topSquare.col].hasTopWall != true && squares[topSquare.row + 1][topSquare.col].visited == false) {
            solution.push(squares[topSquare.row + 1][topSquare.col])
            solution.peek().visited = true
            return true
        } 
        return false
    }
}
