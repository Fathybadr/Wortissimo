from threading import Thread, Lock
import time
import nltk
import random
from nltk.corpus import words
import enchant
from console.utils import wait_key
import sys


nltk.download('words')
dictionary = enchant.Dict("en_US")


def word_finder():
    wordlist = words.words()
    random.shuffle(wordlist)
    wordlist = wordlist[:200]
    wordlist = [w for w in wordlist if 11 <= len(w) <= 12]

    return wordlist


randomWord = random.choice(word_finder())
print(randomWord)


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
                    checkedWordLowercase = notCheckedWord.lower()
                    solutionArray.append(checkedWordLowercase)
            j = j+1
        i = i + 1
    # print(solutionArray)
    return solutionArray
# solution_finder(randomWord)

# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/


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
        G.prompt = f'[WORD: \033[1;31m{G.word}\u001b[0m] [REMAINING TIME \033[1;31m{timerVar}\u001b[0m] Please input solutions: '
        rePrintLine()
        if timerVar == 0:
            break
        pass
    print(
        '\r' + (''.join([' ' for i in range(G.maxLineLength)])) + '\r', end='')
    print(
        "Once you are ready to continue - simply press the '\033[1;32mENTER\u001b[0m' key.")
    #sys.stdin.write(' ')
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


word = "testing"
userInputs = timedUserInput(word)
for singleInput in userInputs:
    print(f'{singleInput}')
print('Something else')

# \/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/
