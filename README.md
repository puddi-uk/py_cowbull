# python_exercises

## cowbull.py

An implementation of the game "Mastermind" where a player tries to guess a random number. Each guess made they are told how many "bulls" and "cows" they scored, where:
* A bull is a digit in the guess which matches at the same index as the target, e.g. A guess of "020" for target "121" scores a bull for the 2.
* A cow is a digit in the guess which is contained in the target but at a different index and which isn't a bull, e.g. A guess of "200" for target "112" scores a cow for the 2.
