# Dashiell Coyier 2/17/2026 (Linear Algebra)

# Code for calculating free variables in large matrices that represent the Lights Out game
# http://www.brianveitch.com/games/Lights-Out/index.html


# Need to install wolframclient
# Use First@$CommandLine in Mathematica to find wolfram kernel

# imports
from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl


# builds a lights out nxn matrix
def buildMatrix(n):
    matrixRows = []

    entries = n * n

    # make each row
    for i in range(1, entries + 1):
        matrixRow = []

        # finding adjacents
        for a in range(1, entries + 1):
            if (
                a == i - n
                or (a == i - 1 and i % n != 1)
                or a == i
                or (a == i + 1 and i % n != 0)
                or a == i + n
            ):
                matrixRow.append(1)
            else:
                matrixRow.append(0)

        matrixRows.append(matrixRow)

    return matrixRows


def printMatrix(matrix):
    # top border
    border = ""
    for item in matrix[0]:
        border += "-"
    border += "--"
    print(border)

    # matrix
    for list in matrix:
        row = "|"
        for item in list:
            if item == 0:
                row += " "
            else:
                row += "1"
        row += "|"
        print(row)

    # bottom border
    border = ""
    for item in matrix[0]:
        border += "-"
    border += "--"
    print(border, "\n")


def printMatrixAndRowReduced(n):
    matrix = buildMatrix(n)
    reduced = session.evaluate(wl.RowReduce(matrix, Modulus=2))
    printMatrix(matrix)
    print()
    printMatrix(reduced)


if __name__ == "__main__":
    session = WolframLanguageSession(
        "/Volumes/Wolfram/Wolfram.app/Contents/MacOS/WolframKernel"
    )

    printMatrixAndRowReduced(8)

    noFreeVars = []

    print("Row -> Rank, Free vars\n---------")
    for i in range(2, 41):
        matrix = buildMatrix(i)
        rank = session.evaluate(wl.MatrixRank(matrix, Modulus=2))
        print(f"{i} -> {rank}, {i * i - rank}")
        if i * i == rank:
            noFreeVars.append(i)

    line = ""
    for n in noFreeVars:
        if (n * n) % 2 == 1:
            print(n)
    # print(noFreeVars)
    for i in range(2, 41):
        inNoFreeVars = False
        for n in noFreeVars:
            if i == n:
                line += "o"
                inNoFreeVars = True

        if not inNoFreeVars:
            line += "-"

    print(line)

    session.terminate()
