import random

NUMBER_LENGTH = 4

def determineCowsBulls(targetArray, playerArray):

    cows = 0
    bulls = 0
    
    # Store the index of each "bull" found so that it's not double counted when checking for "cows"
    bullIndices =  []

    # Count "bulls" (digits occuring at the same index in both arrays) and store the index to avoid counting them as "cows" later.
    for digit in range(NUMBER_LENGTH):

        if playerArray[digit] == targetArray[digit]:
            bulls = bulls + 1;
            bullIndices.append(digit)
     
    # Count "cows" (digits occurring at any index in the targetArray but which weren't a "bull").
    for digit in range(NUMBER_LENGTH):

        if (not digit in bullIndices) and (playerArray[digit] in targetArray):
            cows = cows + 1
    
    return [cows,bulls]
   
    
def intToArray(intNumber):
    numberAsString = str(intNumber)
    array = []
    for i in range(len(numberAsString)):
        array.append(numberAsString[i])
        
    return array
 
 
def generateTargetNumber():
    # Lowest number with NUMBER_LENGTH digits. E.g. for NUMBER_LENGTH 4 we do 10^3 = 1000
    minTargetValue = pow(10,NUMBER_LENGTH - 1)
    # Largest number with NUMBER_LENGTH digits. E.g. for NUMBER_LENGTH 4 we do 10^4-1 = 9999
    maxTargetValue = pow(10,NUMBER_LENGTH) - 1
    
    return random.randint(minTargetValue, maxTargetValue)


def gameLoop(targetNumber = generateTargetNumber()):
    
    targetArray = intToArray(targetNumber)
    
    numberOfGuesses = 0
    
    # Loop until player quits or wins.
    guessing = True
    while guessing:
        playerInput = input("Your guess: ")
        if playerInput == "q":
            print("Bye!")
            return
        
        playerArray = intToArray(playerInput)
        
        if len(playerArray) != NUMBER_LENGTH:
            print("Guess must be " + str(NUMBER_LENGTH) + " digits long.")
            continue
        
        numberOfGuesses = numberOfGuesses + 1
        cowsBulls = determineCowsBulls(targetArray, playerArray)
        
        print("Score: " + str(cowsBulls[1]) + " bulls & " + str(cowsBulls[0]) + " cows.\n")
        
        if cowsBulls[1] == NUMBER_LENGTH:
            print("Victory in " + str(numberOfGuesses) + " guesses!")
            guessing = False


# Good test data: 3388 -> 3838 8383 8833
gameLoop()
