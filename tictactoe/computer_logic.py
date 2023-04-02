from constants import *
import random
import grid_util

def takeTurn(grid, movesRemaining):
    # The center cell is of strategic importance, so begin by identifying it.
    centerCell = grid_util.calcCenterCell(grid)

    # If this is the first move, the best strategy is to play in the centre cell.
    if (movesRemaining == GRID_CELL_COUNT):
        return playInCell(grid, centerCell)

    # It is turn 2+ so we need to identify potential moves then identify the best one. 
    blankCells = grid_util.getBlankCells(grid)
    
    return playOptimalMove(grid, blankCells, centerCell)


def playOptimalMove(grid, blankCells, centerCell): 

    # Invalid values, but avoids None checks later on. 
    bestMoveScore = -1
    bestMoveCell  = -1
    
    for consideredCell in blankCells:
        # Get the row and column containing the cell we might play. 
        rowCells = grid_util.getRowContainingCell(grid, consideredCell)
        colCells = grid_util.getColContainingCell(grid, consideredCell)
        # Get the diagonals containing the cell we might play (though no valid diagonal may exist).
        tlbrDiagCells = grid_util.getTLBRDiagContainingCell(grid, consideredCell)
        trblDiagCells = grid_util.getTRBLDiagContainingCell(grid, consideredCell)

        score = scorePotentialMove(rowCells, colCells, tlbrDiagCells, trblDiagCells)

        # If the move being considered results in an immediate win or prevents the human from winning then
        # simply play that move and skip considering any others.
        if (score == SCORE_COMPUTER_VICTORY or score == SCORE_PREVENT_HUMAN_VICTORY):
            return playInCell(grid, consideredCell)
        
        # If we're considering the center tile and it's blank, add a bit of preferential bias.
        if (consideredCell == centerCell) and (grid[centerCell] == BLANK_CELL_VALUE):
                score = score + SCORE_CENTER_CELL_BIAS
        
        # If the move being considered is better than the best we've found so far update it to be our best move.
        if (score > bestMoveScore):
            bestMoveScore = score
            bestMoveCell = consideredCell

    # There was no immediate win/human-blocking move, so play the best we've identified.
    return playInCell(grid, bestMoveCell)
        


def scorePotentialMove(rowCells, colCells, tlbrDiagCells, trblDiagCells):
    rowTotal = sum(rowCells)
    colTotal = sum(colCells)
    tlbrDiagTotal = sum(tlbrDiagCells)
    trblDiagTotal = sum(trblDiagCells)

    lineTotals = [rowTotal, colTotal, tlbrDiagTotal, trblDiagTotal] 

    # The best move is one that allows the computer to win; no further scoring is needed.
    if(resultsInComputerVictory(lineTotals) == True):
        return SCORE_COMPUTER_VICTORY
    # The next best move is one that prevents the human from winning on their next move; no further scoring is needed.
    elif (preventsHumanVictory(lineTotals) == True):
        return SCORE_PREVENT_HUMAN_VICTORY
    else:
        return calculateScoreForLines(lineTotals)


def calculateScoreForLines(lineTotals):
    scoreForLines = 0

    for line in range(len(lineTotals)):
        scoreForLines = scoreForLines + scoreLine(lineTotals[line])

    return scoreForLines


def scoreLine(line):
    score = 0

    while (line > 0):
        if (line >= COMPUTER_CELL_VALUE):
            line = line - COMPUTER_CELL_VALUE
            score = score + SCORE_COMPUTER_CELL_ON_LINE
            continue
        if (line >= HUMAN_CELL_VALUE):
            line = line - HUMAN_CELL_VALUE
            score = score + SCORE_HUMAN_CELL_ON_LINE

    return score


def resultsInComputerVictory(lineTotals):
    for i in range(len(lineTotals)):
        if (lineTotals[i] == COMPUTER_WIN_LINE_VALUE):
            return True
    return False


def preventsHumanVictory(lineTotals):
    for i in range(len(lineTotals)):
        if (lineTotals[i] == HUMAN_PENULTIMATE_WIN_VALUE):
            return True
    return False


def playInCell(grid, cell):
    newGrid = grid.copy()
    newGrid[cell] = COMPUTER_CELL_VALUE
    return newGrid


# Generate all possible grids that can result of the computer taking its turn.
def generatePotentialMoveOutcomes(grid, movesRemaining):
    potentialMoveOutcomeGrids = []
    
    # Only need to check grids with valid moves, hence only those with moves remaining.
    movesLeftToCheck  = movesRemaining

    # While there are moves still to check...
    nextCellToCheck = 0
    while (movesLeftToCheck > 0):
        # Step through the cells, starting at the next cell we should check (so we don't keep checking the same move).
        for cell in range(nextCellToCheck, len(grid), 1):
            # If the cell is blank, it's a potential legal move, so create a grid representing that more and store it.
            if (grid[cell] == BLANK_CELL_VALUE):
                newGrid = grid.copy()
                newGrid[cell] = COMPUTER_CELL_VALUE
                potentialMoveOutcomeGrids.append(newGrid)
                # As a move has been generated for this cell we should only consider the next cell as a potential move.
                # We've also found one of the potential moves thus we have one less to check, so move onto the next potential move.
                nextCellToCheck = nextCellToCheck + 1
                movesLeftToCheck = movesLeftToCheck - 1
                break

    return potentialMoveOutcomeGrids




