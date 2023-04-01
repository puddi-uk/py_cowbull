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
        cellIndex = i * (GRID_SIDE_LENGTH - 1)
        total = total + grid[cellIndex]
    return total

def calcCenterCellIndexes(grid):
    centerCellIndexes = [] 

    halfSideLength = GRID_SIDE_LENGTH // 2 
    
    # If the grid has an odd side length there is a single central cell.
    if (GRID_SIDE_LENGTH % 2 != 0):
        # halfSideLength is the depth (number of rows before the center row).
        cellsInRowsAboveCenterRow = halfSideLength * GRID_SIDE_LENGTH
        # halfSideLength is also the number of cells in a row before the center cell.
        cellsInRowBeforeCenter = halfSideLength
    # Else the grid has an even side length so there are multiple central cells.
    else:

    # Therefore the centreCellIndex is the number of cells in the rows above plus the number of cells in the center row preceeding it.
    centerCellIndex = cellsInRowsAboveCenterRow + cellsInRowBeforeCenter

def calculateMaximumScoreForGrid(grid):
    maximumScore = 0
    # Score rows/cols.
    for i in range(GRID_SIDE_LENGTH):
        score = scoreCol(grid, i)
        if (score > maximumScore):
            maximumScore = score
    for i in range(GRID_SIDE_LENGTH):
        score = scoreRow(grid, i)
        if (score > maximumScore):
            maximumScore = score
    # Score diags.
    score = scoreDiagTLBR(grid)
    if (score > maximumScore):
        maximumScore = score
    score = scoreDiagTRBL(grid)
    if (score > maximumScore):
        maximumScore = score
    return maximumScore


def getWinnerForScore(score):
    if (score == HUMAN_WIN_LINE_VALUE):
        return HUMAN_NAME
    elif (score == COMPUTER_WIN_LINE_VALUE):
        return COMPUTER_NAME
    else:
        return None


def getWinner(grid):
    maximumScore = calculateMaximumScoreForGrid(grid)
    return getWinnerForScore(maximumScore)


def init():
    grid = []
    for i in range(GRID_CELL_COUNT):
        grid.append(BLANK_CELL_VALUE)
    return grid