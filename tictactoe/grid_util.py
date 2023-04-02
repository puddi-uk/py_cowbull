from constants import *

def draw(grid):
    print()

    # Counts the number of columns drawn in a row, allows insertion of a linebreak at the end of the row.
    numberOfColumnsDrawn = 0 
    
    for i in range(GRID_CELL_COUNT):
        
        # Insert a line break if we're on the next row down.
        if (numberOfColumnsDrawn == GRID_SIDE_LENGTH):
            print()
            numberOfColumnsDrawn = 0

        # If this is the first column, insert an axis label (flipping the label value to index from bottom as it's more intuitive for humans)
        if (numberOfColumnsDrawn == 0):
            axisLabel = int( (GRID_SIDE_LENGTH - 1) - (i / GRID_SIDE_LENGTH) )
            print(f'{axisLabel} ', end='')
        
        # Lookup the cell symbol and draw it.
        print(f'{SYMBOL_DICTIONARY[grid[i]]} ', end='')
      
        numberOfColumnsDrawn = numberOfColumnsDrawn + 1
        
    # Draw axis labels along the bottom.
    print("\n  ", end='')
    for i in range(GRID_SIDE_LENGTH):
        print(f'{i} ', end='')
        
    # Finally add a line break to avoid further printing on the axis line.
    print()


def scoreCol(grid, rowIndex):
    # Slice from the index at the start of the column, end at the end of the grid.
    # Step by GRID_SIDE_LENGTH as moving "down" the grid, indexes are not consecutive.
    return sum(grid[rowIndex : GRID_CELL_COUNT : GRID_SIDE_LENGTH])


def scoreRow(grid, rowIndex):
    # Slice from the index at the start of the row, ending at the index at the end of the row (+ GRID_SIDE_LENGTH).
    # Step by 1 as we're going along the row and thus along consecutive indexes.
    return sum(grid[rowIndex * GRID_SIDE_LENGTH : rowIndex * GRID_SIDE_LENGTH + GRID_SIDE_LENGTH : 1])


def scoreDiagTLBR(grid):
    return sum(grid[0 : GRID_CELL_COUNT : GRID_SIDE_LENGTH + 1])


def scoreDiagTRBL(grid):
    total = 0
    for i in range(1, GRID_SIDE_LENGTH + 1):
        cell = i * (GRID_SIDE_LENGTH - 1)
        total = total + grid[cell]
    return total


def calcCenterCell(grid):
    halfSideLength = GRID_SIDE_LENGTH // 2 
    
    # halfSideLength is the depth (number of rows before the center row).
    cellsInRowsAboveCenterRow = halfSideLength * GRID_SIDE_LENGTH
    # halfSideLength is also the number of cells in a row before the center cell.
    cellsInRowBeforeCenterCell = halfSideLength
    # The center cell index is thus all those in the rows above plus all those in the same row as the center cell which preceed the center cell itself.
    return cellsInRowsAboveCenterRow + cellsInRowBeforeCenterCell


def getBlankCells(grid):
    blankCells = []
    for cell in range(len(grid)):
        if (grid[cell] == BLANK_CELL_VALUE):
            blankCells.append(cell)
    return blankCells


def getRowContainingCell(grid, targetCell):
    for i in range(GRID_SIDE_LENGTH):
        rowStartIndex = i * GRID_SIDE_LENGTH
        rowIndexes = list(range(rowStartIndex, rowStartIndex + GRID_SIDE_LENGTH))
        if (targetCell in rowIndexes):
            return grid[rowStartIndex : rowStartIndex + GRID_SIDE_LENGTH : 1]


def getColContainingCell(grid, targetCell):
    for colStartIndex in range(GRID_SIDE_LENGTH):
        colIndexes = list(range(colStartIndex, GRID_CELL_COUNT, GRID_SIDE_LENGTH))
        if (targetCell in colIndexes):
            return grid[colStartIndex : GRID_CELL_COUNT: GRID_SIDE_LENGTH]


def getTLBRDiagContainingCell(grid, targetCell):
    tlbrCells = grid[0 : GRID_CELL_COUNT : GRID_SIDE_LENGTH + 1]
    if (targetCell in tlbrCells):
        return tlbrCells
    else:
        return []


def getTRBLDiagContainingCell(grid, targetCell): 
    # Work out what the indexes are of cells along the diagonal.
    trblCellIndexes = []
    for i in range(1, GRID_SIDE_LENGTH + 1):
        cellIndex = i * (GRID_SIDE_LENGTH - 1)
        trblCellIndexes.append(cellIndex)

    # If the targetCell is on this diagonal return the cell values of that diagonal.
    tlbrCellValues = []
    if targetCell in trblCellIndexes:
        for i in range (len(trblCellIndexes)):
            tlbrCellValues.append(grid[i])
    return tlbrCellValues


def getWinnerForScore(score):
    if (score == HUMAN_WIN_LINE_VALUE):
        return HUMAN_NAME
    elif (score == COMPUTER_WIN_LINE_VALUE):
        return COMPUTER_NAME
    else:
        return None


def evaluateDiagsForWinner(grid):
    winner = getWinnerForScore(scoreDiagTLBR(grid))
    if (winner != None):
        return winner
    winner = getWinnerForScore(scoreDiagTRBL(grid))
    if (winner != None):
        return winner
    return None


def evaluateColsForWinner(grid):
    for colNum in range(GRID_SIDE_LENGTH):
        winner = getWinnerForScore(scoreCol(grid, colNum))
        if (winner != None) :
            return winner
    return None
        

def evaluateRowsForWinner(grid):
    for rowNum in range(GRID_SIDE_LENGTH):
        winner = getWinnerForScore(scoreRow(grid, rowNum))
        if (winner != None) :
            return winner
    return None
        

def getWinner(grid):
    winner = evaluateRowsForWinner(grid)
    if (winner != None):
        return winner

    winner = evaluateColsForWinner(grid)
    if (winner != None):
        return winner

    winner = evaluateDiagsForWinner(grid)
    return winner


def init():
    grid = []
    for i in range(GRID_CELL_COUNT):
        grid.append(BLANK_CELL_VALUE)
    return grid