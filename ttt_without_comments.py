import msvcrt
import sys


def isDone(pzl, filledPos):
    winstr = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
              {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {6, 4, 2}]
    if filledPos < 5:
        return False, 0
    for cstr in winstr:
        if allXs(pzl, cstr):
            return True, 1
        elif allOs(pzl, cstr):
            return True, -1
    if filledPos == 9:
        return True, 0
    return False, 0

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

def categorizeMoves(pzl):
    if pzl == '.' * 9:
        return set(), set(), {4, 0, 2, 6, 8, 1, 3, 5, 7}
    currentPlayer = 'x' if pzl.count('.') % 2 else 'o'
    solved, result = isDone(pzl, 9 - pzl.count('.'))
    if solved:
        if result == -1 and currentPlayer == 'x':
            return set(), {-1}, set()
        elif result == 1 and currentPlayer == 'x':
            return {-1}, set(), set()
        elif result == 0:
            return set(), set(), {-1}
        elif result == -1 and currentPlayer == 'o':
            return {-1}, set(), set()
        elif result == 1 and currentPlayer == 'o':
            return set(), {-1}, set()
    good, bad, tie = set(), set(), set()
    possMoves = {index for index, chr in
                 enumerate(pzl) if chr == '.'}
    for move in possMoves:
        newPzl = pzl[:move] + currentPlayer + pzl[move + 1:]
        oppGood, oppBad, oppTie = categorizeMoves(newPzl)
        if oppGood:
            bad.add(move)
        elif oppTie:
            tie.add(move)
        else:
            good.add(move)

    return good, bad, tie

def checkExit(inp):
    if ord(inp) == 27:
        exit('Game ended.')
    return inp

def getInp(prompt):
    if len(sys.argv) == 2:
        inpt = sys.argv[1].lower()
        if len(inpt) == 1 and inpt in 'xo':
            return inpt
        elif len(inpt) != 9:
            print('Input wasn\'t the size of a tic-tac-toe board.')
        elif {ch for ch in inpt} != {'.', 'o', 'x'} and {ch for ch in inpt} != {'.', 'o'} \
                and {ch for ch in inpt} != {'.', 'x'} and {ch for ch in inpt} != {'.'}:
            print('Input wasn\'t a board -- character besides x, o, or \'.\'')
        elif inpt.count('o') > sys.argv[1].count('x'):
            print('Input wasn\'t a legal board (more o\'s than x\'s).')
        else:
            return inpt
    print(prompt)
    tkn = str(checkExit(msvcrt.getch()))
    return tkn.lower()

def getMove(prompt, board):
    print(prompt)
    while True:
        inp = str(checkExit(msvcrt.getch()))
        if inp[2] not in '012345678':
            print('That\'s not a move. Try again.')
            continue
        inp = int(inp[2])
        if board[inp] != '.':
            print('That\'s taken. Move where?')
            continue
        return inp

def getNextToken(pzl):
    if pzl.count('.') % 2:
        return 'x'
    return 'o'

def getPredictions(good, bad, tie):
    predictions = 'W: (' + ', '.join ([str(i) for i in good]) if good else 'W: (none'
    predictions += ') L: (' + ', '.join ([str(i) for i in bad]) if bad else ') L: (none'
    predictions += ') T: (' + ', '.join ([str(i) for i in tie]) + ')' if tie else ') T: (none)'
    return predictions

def makeMove(pzl, moveIndex, token):
    return pzl[:moveIndex] + token + pzl[moveIndex + 1:]

def setStartVals(inp):
    if len(inp) == 4:
        personTkn = inp[2] if inp[2] in 'xo' else 'x'
        cptrTkn = 'o' if personTkn == 'x' else 'x'
        board = '.' * 9
        numMoves = 0
    elif len(inp) == 1:
        personTkn = inp
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

def printPzl(pzl):
    print(' '.join(pzl[:3]))
    print(' '.join(pzl[3:6]))
    print(' '.join(pzl[6:]))

def play():
    print('Game started. Press \'Esc\' to exit.')
    inp = getInp('X or O? If you press another key, you\'re X.')
    personTkn, cptrTkn, personTurn, board, numMoves = setStartVals(inp)
    print('Your token is: {} Computer\'s token is: {}'.format(personTkn, cptrTkn))
    printPzl(board)
    while True:
        if msvcrt.kbhit():
            checkExit(msvcrt.getch())
        if numMoves % 2 == personTurn:
            move = getMove('Make a move on the above board.', board)
            board = makeMove(board, move, personTkn)
            numMoves += 1
            printPzl(board)
            done, result = isDone(board, numMoves)
            if done:
                output = 'Wow! You just won.' if result != 0 else 'Its a tie :O'
                exit(output)
        else:
            good, bad, tie = categorizeMoves(board)
            move = [*good, *tie, *bad][0]
            predictions = getPredictions(good, bad, tie)
            board = makeMove(board, move, cptrTkn)
            print('Computer placed {} at index {} of choices: {}'
                  .format(cptrTkn, move, predictions))
            printPzl(board)
            numMoves += 1
            done, result = isDone(board, numMoves)  # check whether game is done
            if done:
                output = 'Wow! You just lost. That sucks.' if result != 0 * personTurn else 'It\'s a tie :O'
                exit(output)
play()
