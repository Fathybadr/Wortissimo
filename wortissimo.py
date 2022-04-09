# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # Import Settings

from wordfreq import zipf_frequency
from threading import Thread, Lock
from console.utils import wait_key
import time
import enchant
import random
import sys
import nltk
from nltk.corpus import words
nltk.download('words')
dictionary = enchant.Dict("en_US")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # The butcher's code-factory threading-hell


class globalVars():
    pass


G = globalVars()


def rePrintLine():
    printStr = f'\r{G.prompt}{G.userInput}'
    G.maxLineLength = max(G.maxLineLength, len(printStr))
    if G.lastStringLength > len(printStr):
        print('\r' + (''.join([' ' for i in range(G.maxLineLength)])), end='')
    G.lastStringLength = len(printStr)
    print(f'\r{printStr}', end='')


def backgroundTask():
    timerVar = 60
    while True:
        time.sleep(1)
        timerVar -= 1
        G.prompt = f'[REMAINING TIME \033[1;31m{timerVar}\u001b[0m] Please input solutions: '
        rePrintLine()
        if timerVar == 0:
            break
        pass
    print(
        '\r' + (''.join([' ' for i in range(G.maxLineLength)])) + '\r', end='')
    print(
        "Once you are ready to continue - simply press the '\033[1;32mENTER\u001b[0m' key.")
    print("\n")
    # sys.stdin.write(' ')
    G.taskEnded = True
    pass


def mainTask():
    while(True):
        userInput = wait_key()
        if G.taskEnded:
            return
        if userInput == '\x08':
            G.userInput = G.userInput[:-1]
        elif userInput == '\r':
            G.enteredStrings.append(G.userInput)
            G.userInput = ''
        else:
            G.userInput += userInput
        rePrintLine()
    pass


def timedUserInput(word):
    G.lock = Lock()
    G.kill = False
    G.taskEnded = False
    G.prompt = ''
    G.userInput = ''
    G.maxLineLength = 0
    G.lastStringLength = 0
    G.enteredStrings = []
    G.word = word
    timerThread = Thread(target=backgroundTask)
    timerThread.start()
    while not G.taskEnded:
        mainTask()
        pass
    timerThread.join()
    return G.enteredStrings
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # The butcher's code-factory
def word_finder():
    wordlist = words.words()
    random.shuffle(wordlist)
    wordlist = wordlist[:200]
    wordlist = [w for w in wordlist if 11 <= len(w) <= 12]

    return wordlist


def solution_finder(word):
    solutionArray = []
    i = 0
    while i < len(word):
        j = i + 1
        while j <= len(word):
            notCheckedWord = (word[i:j])
            # print(notCheckedWord)
            if(len(notCheckedWord) >= 2):
                if(dictionary.check(notCheckedWord)):
                    solutionArray.append(notCheckedWord)
            j = j+1
        i = i + 1
    # print(solutionArray)
    return solutionArray


def ruleQuestion():
    ruleString = input(
        "Do you wish to learn the rules? (\033[1;32myes\u001b[0m/\u001b[31mno\u001b[0m)  ")
    ruleStringLowercase = ruleString.lower()
    if (ruleStringLowercase == "yes"):
        switchRules(1)
    elif (ruleStringLowercase == "no"):
        switchRules(2)
    else:
        switchRules(3)


def switchRules(case):
    if case == 1:  # (YES) --- RULES
        print("Once the game begins - you will have a minute to filter out all the words included within the one displayed to you.")
        print("Write down all the valid words contained within...and perhaps you might even beat me! Ha! Ha! Ha!")
        print("\n")
        input(
            "Once you are ready - simply press the '\033[1;32mENTER\u001b[0m' key.")
    elif case == 2:
        # (NO)
        print("\033[1;31mNext,...\u001b[0m")
    else:  # Anything invalid
        print("- \033[1;31mDEAD WRONG!!! TRY AGAIN!!!\u001b[0m -")
        ruleQuestion()


def difficultyQuestion():
    difficultyInt = input(
        "Choose the difficulty of your opponent! (\033[1;32m1\u001b[0m/\u001b[33m2\u001b[0m/\u001b[31m3\u001b[0m)  ")  # (1/2/3) Lowest ---> Highest
    # DEBUG AAHHAHAHAHHHHH!!!
    # print(type(int(difficultyInt)))
    # print(difficultyInt)
    try:
        if (int(difficultyInt) == 1):
            switchDifficulty(1)
        elif (int(difficultyInt) == 2):
            switchDifficulty(2)
        elif (int(difficultyInt) == 3):
            switchDifficulty(3)
        else:
            switchDifficulty(4)
    except:
        switchDifficulty(4)


def switchDifficulty(case):
    global difficulty
    if case == 1:
        print("\033[1;32mYou want to be spared? What a pity.\u001b[0m")
        difficulty = 1
    elif case == 2:
        print("\033[1;33mA decent challenge! Hah!\u001b[0m")
        difficulty = 2
    elif case == 3:
        print("\033[1;31mPrepare for a world of hurt! Gnarf!\u001b[0m")
        difficulty = 3
    else:  # Anything invalid
        print("- \033[1;31mCHOOSE A VALID DIFFICULTY!!! TRY AGAIN!!!\u001b[0m -")
        difficultyQuestion()


def removeDouble(wordList):
    noDoubleList = list(set(wordList))
    return noDoubleList


def getUserScore(userList, solutionList):
    score = 0
    score = sum(el in userList for el in solutionList)
    return score


def getValidUserSolutions(userSolutions, validSolutions):
    matchingArray = []
    for word in userSolutions:
        if word in validSolutions:
            matchingArray.append(word)
    return matchingArray


def getTempInt(currentWord):
    tempInt = zipf_frequency(currentWord, "en", wordlist='best', minimum=0.)
    return tempInt


def getComputerScore(difficulty, solutionList):
    computerScore = 0
    computerTempArray = []
    if difficulty == 1:
        for currentWord in solutionList:
            tempInt = getTempInt(currentWord)
            if tempInt >= 6:
                computerTempArray += [currentWord]
        computerScore = len(computerTempArray)
        return computerScore, computerTempArray
    elif difficulty == 2:
        for currentWord in solutionList:
            tempInt = getTempInt(currentWord)
            if tempInt >= 4:
                computerTempArray += [currentWord]
        computerScore = len(computerTempArray)
        return computerScore, computerTempArray
    elif difficulty == 3:
        for currentWord in solutionList:
            tempInt = getTempInt(currentWord)
            if tempInt >= 3:
                computerTempArray += [currentWord]
        computerScore = len(computerTempArray)
        return computerScore, computerTempArray


def restartQuestion():
    ruleString = input(
        "Do you wish to restart the game? (\033[1;32myes\u001b[0m/\u001b[31mno\u001b[0m)  ")
    ruleStringLowercase = ruleString.lower()
    if (ruleStringLowercase == "yes"):
        running = True
        return running
    elif (ruleStringLowercase == "no"):
        running = False
        return running
    else:
        print("- \033[1;31mDEAD WRONG!!! TRY AGAIN!!!\u001b[0m -")
        restartQuestion()


def scoreCelebration(userScore, computerScore, solutionList, userList, computerList):
    maximumScore = len(solutionList)
    if userScore == computerScore:
        print("[------------------------------]")
        print("- \033[1;33mA decent match. A tie it is.\u001b[0m -")
        print("[------------------------------]")
        print("\n")
        print(
            "\033[1;33mVALID SOLUTIONS WOULD HAVE BEEN:\u001b[0m " + str(solutionList))
        print("\033[1;32mYour valid solutions are:\u001b[0m " + str(userList))
        print("\033[1;31mHere are my humble solutions:\u001b[0m " +
              str(computerList))
        print("\n")
        print(
            "\033[1;33mTHE MAXIMUM SCORE ACHIEVABLE IS:\u001b[0m " + str(maximumScore))
        print("\033[1;32mYour equally 'ok' score is:\u001b[0m " + str(userScore))
        print(
            "\033[1;31mA tie...and so we share the same score:\u001b[0m " + str(computerScore))
        print("\n")
    elif userScore > computerScore:
        print("[-----------------------------------]")
        print("- \033[1;32mYou won...congratulations,... >_>\u001b[0m -")
        print("[-----------------------------------]")
        print("\n")
        print(
            "\033[1;33mVALID SOLUTIONS WOULD HAVE BEEN:\u001b[0m " + str(solutionList))
        print(
            "\033[1;32mYour 'many' valid solutions are:\u001b[0m " + str(userList))
        print(
            "\033[1;31mAt least I still got a few good solutions:\u001b[0m " + str(computerList))
        print("\n")
        print(
            "\033[1;33mTHE MAXIMUM SCORE ACHIEVABLE IS:\u001b[0m " + str(maximumScore))
        print("\033[1;32mYour 'winning' score is:\u001b[0m " + str(userScore))
        print(
            "\033[1;31mDespite everything I still have a score of:\u001b[0m " + str(computerScore))
        print("\n")
    else:  # userScore < computerScore
        print("[-----------]")
        print("- \033[1;31mLOSER!!!\u001b[0m -")
        print("[-----------]")
        print("\n")
        print(
            "\033[1;33mVALID SOLUTIONS WOULD HAVE BEEN:\u001b[0m " + str(solutionList))
        print("\033[1;32mYour few valid solutions are:\u001b[0m " + str(userList))
        print("\033[1;31mI on the other hand won by sending in these splendid solutions:\u001b[0m " + str(computerList))
        print("\n")
        print(
            "\033[1;33mTHE MAXIMUM SCORE ACHIEVABLE IS:\u001b[0m " + str(maximumScore))
        print("\033[1;32mYour score is:\u001b[0m " + str(userScore))
        print(
            "\033[1;31mHowever I reign supreme with the unbeatable score of:\u001b[0m " + str(computerScore))
        print("\n")
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # Runtime-Kingdom! Wowza! \[T]/
running = True
while running == True:
    print("[----------------------------]")
    print("- \033[1;31mWELCOME TO THE BUTCHERY!!!\u001b[0m -")
    print("[----------------------------]")
    ruleQuestion()
    difficultyQuestion()
    input(
        "Once you are ready to begin the game - simply press the '\033[1;32mENTER\u001b[0m' key.")
    print("\n")
    # wordArray = getWordArray()
    # word, solutionArray = splitWordArray(wordArray)
    word = random.choice(word_finder())
    solutionArray = solution_finder(word)
    print("[----------------------------]")
    print("- THE WORD IS: \033[1;31m" + word + "\u001b[0m -")
    print("[----------------------------]")
    print("\n")

    # Begin threading task! Timer and all that mumbo-jumbo! c:
    userInputs = timedUserInput(word)
    # for singleInput in userInputs:
    #    print(f'{singleInput}')
    # This is a list element too! <3
    userInputsFiltered = removeDouble(userInputs)

    userScore = getUserScore(userInputsFiltered, solutionArray)
    userInputsFilteredValid = getValidUserSolutions(
        userInputsFiltered, solutionArray)

    (computerScore, computerSolutionList) = getComputerScore(
        difficulty, solutionArray)

    scoreCelebration(userScore, computerScore, solutionArray,
                     userInputsFilteredValid, computerSolutionList)

    running = restartQuestion()
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # DEBUG-HELL 666 & NOTES
# Includes the word itself and the valid solutions. Needs to be filtered further - through splitWordArray(array)
# wordArrayDebug = getWordArray()
# print(wordArrayDebug)

# wordDebug, solutionArrayDebug = splitWordArray(wordArrayDebug)
# print(wordDebug)
# print(solutionArrayDebug)

# PrintWord - DONE
# StartTimer - DONE
# Save Inputs - DONE
# End Timer - DONE
# Compare input array to solution array and count score - DONE
# Calculate score of opponent depending on difficulty - DONE
# Ask player to play again. - DONE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - # Various stuff for the slaughtered. D:<
# Rene Buchaly
# Fathy Ahmed
# Omar Farghaly
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - #
