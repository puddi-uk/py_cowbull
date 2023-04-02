import random
import time
import re

import computer_logic
import grid_util
from constants import *

PLAYER_INPUT_VALIDATION_REGEX = re.compile("(\d+) (\d+)")

def readHumanInput():
    isValidInput = False
    
    while True:
        inputString = input("Your move (x y): ")
        
        isMatchingInput = PLAYER_INPUT_VALIDATION_REGEX.match(inputString)
        if (not isMatchingInput):
            print("Invalid input. Format should be 'x y' where x and y are numbers.")
            continue
    
        inputX = int(PLAYER_INPUT_VALIDATION_REGEX.match(inputString).group(1))
        inputY = int(PLAYER_INPUT_VALIDATION_REGEX.match(inputString).group(2))
        
        isValidX = (inputX >= 0) and (inputX < GRID_SIDE_LENGTH)
        isValidY = (inputY >= 0) and (inputY < GRID_SIDE_LENGTH)
        
        if not isValidX or not isValidY:
            print(f'Invalid input. Values of x and y should be between 0 and {GRID_SIDE_LENGTH - 1}.')
        else:
            return [inputX,inputY]


def handleInput(humanInput, grid):
    xPos = humanInput[0]
    yPos = humanInput[1]

    # Flip yPos from its human intuitive version.
    yPos = (GRID_SIDE_LENGTH - 1) - yPos
    
    targetCellIndex = (yPos * GRID_SIDE_LENGTH) + xPos

    if (grid[targetCellIndex] != BLANK_CELL_VALUE):
        print("That cell is already taken!")
        return None
    else:
        grid[targetCellIndex] = HUMAN_CELL_VALUE
        return grid
        

def doComputerTurn(grid, movesRemaining):
    print(f'\n{COMPUTER_NAME}\'s turn...thinking...')
    time.sleep(0.5)
    return computer_logic.takeTurn(grid, movesRemaining)


def doHumanTurn(grid):
    print(f'\n{HUMAN_NAME}\'s turn!')

    # The new state of the game after the human's move.
    newGrid = None

    while newGrid == None:
        humanInput = readHumanInput()
        newGrid = handleInput(humanInput, grid)
    
    return newGrid


def gameLoop():
    grid = grid_util.init()
    
    isHumanTurn = random.choice([True, False])
    movesRemaining = GRID_CELL_COUNT
    
    while True:
        grid_util.draw(grid)
        
        if isHumanTurn:
            grid = doHumanTurn(grid)
        else:
            grid = doComputerTurn(grid, movesRemaining)
            
        movesRemaining = movesRemaining - 1
        
        victor = grid_util.getWinner(grid)
        
        # If we have a winner, the game is over.
        if victor != None:
            grid_util.draw(grid)
            print(f'\nGame over! Result: {victor} wins!')
            return
        # Else If we don't have a winner but no moves remain, the game is drawn.
        elif (movesRemaining == 0):
            grid_util.draw(grid)
            print("\nGame over! Result: Draw")
            return
        # Else it is the next player's turn.
        else:
            isHumanTurn = not isHumanTurn

# It doesn't make sense to play on a 2x2 grid (or smaller) so bail out if so.
if (GRID_SIDE_LENGTH < 3 or GRID_SIDE_LENGTH % 2 == 0):
    print("Playing tic-tac-toe requires a grid with an odd numbered side length which must be 3 or greater. Update GRID_SIDE_LENGTH in constants.py")
    exit(1)
else: 
    gameLoop()