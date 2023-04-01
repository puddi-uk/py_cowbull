import random
import copy

NUMBER_LENGTH = 4
VERBOSE = False

def determineCowsBulls(targetArray, playerArray):

    # Python is pass-by-reference, need to copy the targetArray so changes to it avoid changing the original.
    modifiableTargetArray = copy.deepcopy(targetArray)
    modifiablePlayerArray = copy.deepcopy(playerArray)

    cows = 0
    bulls = 0

    # Count "bulls" (digits occuring at the same index in both arrays) and store the index to avoid counting them as "cows" later.
    for digit in range(NUMBER_LENGTH):
        
        if VERBOSE:
            print(f'\nCounting bulls ({bulls} so far). Considering index {digit}')
            print(f'TARGET: {modifiableTargetArray}')
            print(f'GUESS:  {modifiablePlayerArray}')

        if modifiablePlayerArray[digit] == modifiableTargetArray[digit]:
            bulls = bulls + 1
            # As a bull digit was found remove it from further comparisons.
            modifiableTargetArray[digit] = None
            modifiablePlayerArray[digit] = None

    # Count "cows" (digits occurring at any index in the targetArray but which weren't a "bull").
    for digit in range(NUMBER_LENGTH):
        
        if VERBOSE:
            print(f'\nCounting cows ({cows} so far)... Considering index {digit}')
            print(f'TARGET: {modifiableTargetArray}')
            print(f'GUESS:  {modifiablePlayerArray}')
        
        # Skip checking digits which were bulls.
        if (modifiablePlayerArray[digit] == None):
            continue
        
        # Find the first occurrence of the player's digit in the target array (if it exists).
        firstOccurenceIndex = firstIndexOf(modifiablePlayerArray[digit], modifiableTargetArray)
        
        if (firstOccurenceIndex != None):
            cows = cows + 1
            # As a cow digit was found remove it from the target to avoid double counting.
            modifiableTargetArray[firstOccurenceIndex] = None
            
    return [cows,bulls]
   

def firstIndexOf(integer, array):
    for index in range(len(array)):
        if integer == array[index]:
            return index
    return None

   
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
            print(f'Guess must be {NUMBER_LENGTH} digits long.')
            continue
        
        numberOfGuesses = numberOfGuesses + 1
        cowsBulls = determineCowsBulls(targetArray, playerArray)
        
        print(f'Score: {cowsBulls[1]} bulls & {cowsBulls[0]} cows.\n')
        
        if cowsBulls[1] == NUMBER_LENGTH:
            print(f'Victory in {numberOfGuesses} guesses!')
            guessing = False


# Good test data: 3388 -> 3838 8383 8833
# Good test data: 7614 -> 1111 1777 7111
# Good test data: 4332 -> 1234
gameLoop()