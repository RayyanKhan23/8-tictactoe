import msvcrt
import sys

# tic tac toe part 2 12-5-18

# globals
BOARD = '.' * 9  # default
ALLPOS = {0, 1, 2, 3, 4, 5, 6, 7, 8}
WINSTR = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {6, 4, 2}]
RESULTS = {}


# helpers
def isDone(pzl, filledPos):  # check whether game is finished
    if filledPos < 5:  # impossible to finish if < 5 moves
        return False, 0
    for cstr in WINSTR:
        if allXs(pzl, cstr):  # if there are 3 X's in a row
            return True, 1  # return that it's done with winner X
        elif allOs(pzl, cstr):  # same for O
            return True, -1
    if filledPos == 9:  # if there's no X or O winner but board full
        return True, 0  # it's a draw
    return False, 0


def allXs(pzl, cstr):  # check for 3 X's in a row, col, or diagonal
    for index in cstr:
        if pzl[index] != 'x':
            return False
    return True


def allOs(pzl, cstr):
    for index in cstr:
        if pzl[index] != 'o':
            return False
    return True


def updateResults(filledPos, pzl, result):  # update global results
    if filledPos == 9:  # to include new finished games
        if 9 in RESULTS:
            RESULTS[filledPos].add((pzl, result))
        else:
            RESULTS[filledPos] = {(pzl, result)}
    elif filledPos in RESULTS:
        RESULTS[filledPos].add(pzl)
    else:
        RESULTS[filledPos] = {pzl}


def makeMove(pzl, moveIndex, token):
    return pzl[:moveIndex] + token + pzl[moveIndex + 1:]


def printPzl(pzl):
    print(' '.join(pzl[:3]))
    print(' '.join(pzl[3:6]))
    print(' '.join(pzl[6:]))


def getNextToken(pzl):
    if pzl.count('.') % 2:
        return 'x'
    return 'o'


def getInp(prompt):
    print(prompt)
    return str(checkExit(msvcrt.getch()))


def getMove(prompt, board):
    print(prompt)
    while True:
        inp = int(checkExit(msvcrt.getch()))
        if str(inp) not in '012345678':
            print('That\'s not a move. Try again.')
            continue
        if board[inp] != '.':
            print('That\'s taken. Move where?')
            continue
        return inp


def checkExit(inp):
    if ord(inp) == 27:
        exit('Game ended.')
    return inp


def minimax(pzl):
    if pzl == '.' * 9:
        return set(), set(), [4, 0, 2, 6, 8, 1, 3, 5, 7]

    currentPlayer = 'x' if pzl.count('.') % 2 else 'o'
    solved, result = isDone(pzl, 9 - pzl.count('.'))
    if solved:
        if result == -1 and currentPlayer == 'x':  # good, bad, draw
            return set(), {-1}, set()
        elif result == 0:
            return set(), set(), {-1}
        elif result == 1 and currentPlayer == 'x':
            return {-1}, set(), set()
        elif result == -1 and currentPlayer == 'o':
            return {-1}, set(), set()
        elif result == 1 and currentPlayer == 'o':
            return set(), {-1}, set()

    good, bad, tie = set(), set(), set()
    possMoves = {index for index, chr in enumerate(pzl) if chr == '.'}  # fix/do better later

    for move in possMoves:
        newPzl = pzl[:move] + currentPlayer + pzl[move + 1:]

        oppGood, oppBad, oppTie = minimax(newPzl)
        if oppGood:
            bad.add(move)
        elif oppTie:
            tie.add(move)
        else:
            good.add(move)

    return good, bad, tie


def setStartVals(inp):
    if len(inp) == 4:
        personTkn = inp[0] if inp[0] in 'xo' else 'x'
        cptrTkn = 'o' if personTkn == 'x' else 'x'
        board = '.' * 9
        numMoves = 0
    else:
        cptrTkn = getNextToken(inp)
        personTkn = 'o' if cptrTkn == 'x' else 'x'
        board = inp
        numMoves = 9 - board.count('.')
    personTurn = 0 if personTkn == 'x' else 1
    return personTkn, cptrTkn, personTurn, board, numMoves


def getPredictions(good, bad, tie):
    predictions = 'W: (' + ', '.join([str(i) for i in good]) if good else 'W: (none'
    predictions += ') L: (' + ', '.join([str(i) for i in bad]) if bad else ') L: (none'
    predictions += ') T: (' + ', '.join([str(i) for i in tie]) + ')' if tie else ') T: (none)'
    return predictions


def play():
    inp = sys.argv[1] if len(sys.argv) == 2 else getInp('X or O? If you press another key, you\'re X.')
    personTkn, cptrTkn, personTurn, board, numMoves = setStartVals(inp)

    print('Your token is: {} Computer\'s token is: {}'.format(personTkn, cptrTkn))
    printPzl(board)

    while numMoves != 9:
        if msvcrt.kbhit():
            checkExit(msvcrt.getch())

        if numMoves % 2 == personTurn:  # person's turn
            move = getMove('Make a move on the above board.', board)  # get their move
            board = makeMove(board, move, personTkn)  # make that move
            numMoves += 1
            printPzl(board)
            done, result = isDone(board, numMoves)  # see if it's done and if so result
            if done:
                output = 'Wow! You just won.' if result != 0 else 'Its a tie :O'
                exit(output)

        else:  # computer's turn
            good, bad, tie = minimax(board)
            move = [*good, *tie, *bad][0]
            predictions = getPredictions(good, bad, tie)
            board = makeMove(board, move, cptrTkn)
            print('Computer placed {} at index {}: {}'.format(cptrTkn, move, predictions))
            printPzl(board)
            numMoves += 1
            done, result = isDone(board, numMoves)
            if done:
                output = 'Wow! You just lost. That sucks.' if result != 0 * personTurn else 'It\'s a tie :O'
                exit(output)


play()