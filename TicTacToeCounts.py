
# intro to tic-tac-toe unit
# due 12-3-18, turned in for full credit 12-5 due to Friday absence
# produces tree to find completed tic-tac-toe boards and
# categorize them by win, lose, or draw, and at how many steps

import time
board = '.' * 9
t = time.clock()
allPos = {0, 1, 2, 3, 4, 5, 6, 7, 8}
WINSTR = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {6, 4, 2}]
RESULTS = {}

def isDone(pzl, filledPos):
    if filledPos < 5:
        return False, ''
    for cstr in WINSTR:
        if allXs(pzl, cstr):
            return True, 'X'
        elif allOs(pzl, cstr):
            return True, 'O'
    if filledPos == 9:
        return True, 'D'
    return False, ''

def allXs(pzl, cstr):
    for index in cstr:
        if pzl[index] != 'x':
            return False
    return True

def allOs(pzl, cstr):
    for index in cstr:
        if pzl[index] != 'o':
            return False
    return True

def updateResults(filledPos, pzl, result):
    if filledPos == 9:
        if 9 in RESULTS:
            RESULTS[filledPos].add((pzl, result))
        else:
            RESULTS[filledPos] = {(pzl, result)}
    elif filledPos in RESULTS:
        RESULTS[filledPos].add(pzl)
    else:
        RESULTS[filledPos] = {pzl}

def printPzl(pzl):
    print(' '.join(pzl[:3]))
    print(' '.join(pzl[3:6]))
    print(' '.join(pzl[6:]))

def solvedStates():
    solve(board, 0, allPos)
    print('total states:', len([pz for sub in [RESULTS[k] for k in RESULTS] for pz in sub]))
    for key in RESULTS:
        if key == 9:
            xWins, oWins, draws = 0, 0, 0
            for pzl, gameResult in RESULTS[key]:
                if gameResult == 'X':
                    xWins += 1
                elif gameResult == 'O':
                    oWins += 1
                elif gameResult == 'D':
                    draws += 1
            print('9 steps: X wins {} times'.format(xWins))
            print('9 steps: O wins {} times'.format(oWins))
            print('9 steps: there are {} draws'.format(draws))
        elif key % 2:
            print('{} steps: X wins {} times.'.format(key, len(RESULTS[key])))
        else:
            print('{} steps: O wins {} times.'.format(key, len(RESULTS[key])))

def solve(pzl, filledPos, availablePos):
    solved, result = isDone(pzl, filledPos)
    if solved:
        #print('new solution:')
        #printPzl(pzl)
        updateResults(filledPos, pzl, result)
        return pzl

    for pos in availablePos:
        if filledPos % 2:
            #print('filled pos:', filledPos, 'AvailablePos:', availablePos)
            newPzl = pzl[:pos] + 'o' + pzl[pos + 1:]
            newAvailablePos = availablePos - {pos}
            solve(newPzl, filledPos + 1, newAvailablePos)
        else:
            #print('filled pos:', filledPos, 'AvailablePos:', availablePos)
            newPzl = pzl[:pos] + 'x' + pzl[pos + 1:]
            newAvailablePos = availablePos - {pos}
            solve(newPzl, filledPos + 1, newAvailablePos)


solvedStates()
print('time: {} seconds.'.format(round(time.clock()-t, 3)))
