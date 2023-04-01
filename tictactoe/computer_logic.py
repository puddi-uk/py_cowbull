from constants import *
import time
import grid_util

MOVE_OUTCOME_SCORE_COMPUTER_VICTORY       = 100
MOVE_OUTCOME_SCORE_IMMINENT_HUMAN_VICTORY = 99
MOVE_OUTCOME_SCORE_ADJACENT_TO_SELF       = 2
MOVE_OUTCOME_SCORE_ADJACENT_TO_HUMAN      = 1

def takeTurn(grid, movesRemaining):

    # If this is the first move, the best strategy is to play in the/a centre cell.
    # Fairly unintelligent implementation as we're not scoring the cells themselves, only the relative human/computer positions.
    if (movesRemaining == GRID_CELL_COUNT):
        return generateCenterCellPlayGrid(grid)

    # Either we're on turn 2+ or the 

    potentialMoveOutcomes = generatePotentialMoveOutcomes(grid, movesRemaining)
    # 2D arrays in Python are scary and confusing so scoredOutcomes is a 1D array containing:
    # [ score1, grid1, score2, grid2, ... ]
    classifiedOutcomes = classifyPotentialMoveOutcomes(potentialMoveOutcomes)

# Plays in the center cell of the grid. 
# For a grid with an odd side length there is a specific center cell.
# For a grid with an even side length there are multiple center cells, we play in the bottom right one (as it's the same algorithm).
def generateCenterCellPlayGrid(grid):   
    halfSideLength = GRID_SIDE_LENGTH // 2 
    
    # halfSideLength is the depth (number of rows before the center row).
    cellsInRowsAboveCenterRow = halfSideLength * GRID_SIDE_LENGTH
    # halfSideLength is also the number of cells in a row before the center cell.
    cellsInRowBeforeCenter = halfSideLength

    # Therefore the centreCellIndex is the number of cells in the rows above plus the number of cells in the center row preceeding it.
    centerCellIndex = cellsInRowsAboveCenterRow + cellsInRowBeforeCenter
    
    newGrid = grid.copy()
    newGrid[centerCellIndex] = COMPUTER_CELL_VALUE
    return newGrid


# 4x4 -> 4/2 -> 2
#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
# [5, 6, 9, 10]

# 6x6 -> 6/2 -> 3
#  0  1  2  3  4  5
#  6  7  8  9 10 11
# 12 13 14 15 16 17
# 18 19 20 21 22 23
# 24 25 26 27 28 29
# 30 31 32 33 34 35
#[14,15,20,21]

# Generate all possible grids that can result of the computer taking its turn.
def generatePotentialMoveOutcomes(grid, movesRemaining):
    potentialMoveOutcomeGrids = []
    
    # Only need to check grids with valid moves, hence only those with moves remaining.
    movesLeftToCheck  = movesRemaining

    # While there are moves still to check...
    nextCellIndexToCheck = 0
    while (movesLeftToCheck > 0):
        # Step through the cells, starting at the next cell we should check (so we don't keep checking the same move).
        for cellIndex in range(nextCellIndexToCheck, len(grid), 1):
            # If the cell is blank, it's a potential legal move, so create a grid representing that more and store it.
            if (grid[cellIndex] == BLANK_CELL_VALUE):
                newGrid = grid.copy()
                newGrid[cellIndex] = COMPUTER_CELL_VALUE
                potentialMoveOutcomeGrids.append(newGrid)
                # As a move has been generated for this cell we should only consider the next cell as a potential move.
                # We've also found one of the potential moves thus we have one less to check, so move onto the next potential move.
                nextCellIndexToCheck = nextCellIndexToCheck + 1
                movesLeftToCheck = movesLeftToCheck - 1
                break

    return potentialMoveOutcomeGrids


# No obvious winning move, play randomly.
# return random.choice(potentialMoves)


def classifyPotentialMoveOutcomes(potentialMoves):
    classifiedMoves = []

    for i in range(len(potentialMoves)):
        grid_util.calculateMaximumScoreForGrid






    # Python 2D array syntax is so counter intuitive...numPy Matrix would be better.
    scoredMoves = [None] * len(potentialMoves)
    for i in range(potentialMoves):
        scoredMoves[i] = [None] * 2

    for i in range(potentialMoves):
        #scoredMoves[i][0] = scoreMove(potentialMoves[i])
        scoredMoves[i][1] = potentialMoves[i]


def isNextTurnHumanWin(totalValue):
    return totalValue == HUMAN_PENULTIMATE_WIN_VALUE


