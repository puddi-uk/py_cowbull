import re
import random
import time

GRID_SIDE_LENGTH = 3
GRID_CELL_NUMBER = GRID_SIDE_LENGTH * GRID_SIDE_LENGTH

PLAYER_INPUT_VALIDATION_REGEX = re.compile("(\d) (\d)")

PLAYER_NAME   = "Player"
COMPUTER_NAME = "Computer"

BLANK_SYMBOL    = "."
PLAYER_SYMBOL   = "O"
COMPUTER_SYMBOL = "X"

BLANK_VALUE    = 0
PLAYER_VALUE   = GRID_SIDE_LENGTH
COMPUTER_VALUE = GRID_SIDE_LENGTH + 1

SYMBOL_DICTIONARY = {
    BLANK_VALUE: BLANK_SYMBOL,
    PLAYER_VALUE: PLAYER_SYMBOL,
    COMPUTER_VALUE: COMPUTER_SYMBOL
}

PLAYER_WIN_LINE_VALUE   = GRID_SIDE_LENGTH * PLAYER_VALUE
COMPUTER_WIN_LINE_VALUE = GRID_SIDE_LENGTH * COMPUTER_VALUE


def drawGrid(grid):
    print()

    # Counts the number of columns drawn in a row, allows insertion of a linebreak at the end of the row.
    numberOfColumnsDrawn = 0 
    
    for i in range(GRID_CELL_NUMBER):
        
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


def readPlayerInput():
    isValidInput = False
    
    while True:
        playerInput = input("Your move (x y): ")
        
        isMatchingInput = PLAYER_INPUT_VALIDATION_REGEX.match(playerInput)
        if (not isMatchingInput):
            print("Invalid input. Format should be 'x y' digits")
            continue
    
        inputX = int(PLAYER_INPUT_VALIDATION_REGEX.match(playerInput).group(1))
        inputY = int(PLAYER_INPUT_VALIDATION_REGEX.match(playerInput).group(2))
        
        isValidX = (inputX >= 0) and (inputX < GRID_SIDE_LENGTH)
        isValidY = (inputY >= 0) and (inputY < GRID_SIDE_LENGTH)
        
        if not isValidX or not isValidY:
            print(f'Invalid input. Values of x and y should be between 0 and {GRID_SIDE_LENGTH - 1}.')
        else:
            return [inputX,inputY]


def handleInput(playerInput, grid):
    xPos = playerInput[0]
    yPos = playerInput[1]

    # Flip yPos from its human intuitive version.
    yPos = (GRID_SIDE_LENGTH - 1) - yPos
    
    targetCellIndex = (yPos * GRID_SIDE_LENGTH) + xPos

    if (grid[targetCellIndex] != BLANK_VALUE):
        print("That cell is already taken!")
        return None
    else:
        grid[targetCellIndex] = PLAYER_VALUE
        return grid
        

def evaluateWinner(totalValue):
    if (totalValue == PLAYER_WIN_LINE_VALUE):
        return PLAYER_NAME
    elif (totalValue == COMPUTER_WIN_LINE_VALUE): 
        return COMPUTER_NAME
    else:
        return None


def checkWinCondition(grid):
    # Check rows and columns for a winner using array splitting.
    for i in range(GRID_SIDE_LENGTH):
        # Slice from the index at the start of the column, end at the end of the grid.
        # Step by GRID_SIDE_LENGTH as moving "down" the grid, indexes are not consecutive.
        colTotal = sum(grid[i : GRID_CELL_NUMBER : GRID_SIDE_LENGTH])
        winner = evaluateWinner(colTotal)
        if (winner != None):
            return winner

        # Slice from the index at the start of the row, ending at the index at the end of the row (+ GRID_SIDE_LENGTH).
        # Step by 1 as we're going along the row and thus along consecutive indexes.
        rowTotal = sum(grid[i * GRID_SIDE_LENGTH : i * GRID_SIDE_LENGTH + GRID_SIDE_LENGTH : 1])
        winner = evaluateWinner(rowTotal)
        if (winner != None):
            return winner

    topLeftToBottomRightTotal = sum(grid[0 : GRID_CELL_NUMBER : GRID_SIDE_LENGTH + 1])
    winner = evaluateWinner(topLeftToBottomRightTotal)
    if (winner != None):
        return winner

    topRightToBottomLeftTotal = 0
    for i in range(1, GRID_SIDE_LENGTH + 1):
        cellIndex = i * (GRID_SIDE_LENGTH - 1)
        topRightToBottomLeftTotal = topRightToBottomLeftTotal + grid[cellIndex]
    winner = evaluateWinner(topRightToBottomLeftTotal)
    if (winner != None):
        return winner

    return None


def doPlayerTurn(grid):
    print(f'\n{PLAYER_NAME}\'s turn!')

    # The new state of the game after the player's move.
    newGrid = None

    while newGrid == None:
        playerInput = readPlayerInput()
        newGrid = handleInput(playerInput, grid)
    
    return grid

def generateAllMoveOutcomes(grid, movesRemaining, value):
    moveOutcomes = []
    movesToCheck = movesRemaining
    nextCellIndexToCheck = 0
    while (movesToCheck > 0):
        for cellIndex in range(nextCellIndexToCheck, len(grid), 1):
            if (grid[cellIndex] == BLANK_VALUE):
                newGrid = grid.copy()
                newGrid[cellIndex] = value
                moveOutcomes.append(newGrid)
                nextCellIndexToCheck = nextCellIndexToCheck + 1
                movesToCheck = movesToCheck - 1
                break
    return moveOutcomes


def doComputerTurn(grid, movesRemaining):
    print(f'\n{COMPUTER_NAME}\'s turn...thinking...')
    time.sleep(0.5)
    
    potentialMoves = generateAllMoveOutcomes(grid, movesRemaining, COMPUTER_VALUE)
   
    # Check whether any of the moves result in an outright win, if so, take that move.
    for i in range(len(potentialMoves)):
        victor = checkWinCondition(potentialMoves[i])
        if (victor == COMPUTER_NAME):
            return potentialMoves[i]
    
    # No obvious winning move, play randomly.
    return random.choice(potentialMoves)


def initGrid():
    grid = []
    for i in range(GRID_CELL_NUMBER):
        grid.append(BLANK_VALUE)
    return grid


def gameLoop():
    grid = initGrid()
    isPlayerTurn = random.choice([True, False])
    movesRemaining = GRID_CELL_NUMBER
    
    while True:
        drawGrid(grid)
        
        if isPlayerTurn:
            grid = doPlayerTurn(grid)
        else:
            grid = doComputerTurn(grid, movesRemaining)
            
        movesRemaining = movesRemaining - 1
        
        victor = checkWinCondition(grid)
        
        # If we have a winner, the game is over.
        if victor != None:
            drawGrid(grid)
            print(f'\nGame over! Result: {victor} wins!')
            return
        # Else If we don't have a winner but no moves remain, the game is drawn.
        elif (movesRemaining == 0):
            drawGrid(grid)
            print("\nGame over! Result: Draw")
            return
        # Else it is the next player's turn.
        else:
            #print("\nSwapping turns!")
            isPlayerTurn = not isPlayerTurn

gameLoop()
