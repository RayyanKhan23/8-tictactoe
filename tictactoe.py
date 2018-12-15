# tic tac toe part 2 12-5-18

# globals
START = '.' * 9
ALLPOS = {0, 1, 2, 3, 4, 5, 6, 7, 8}
WINSTR = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6}, {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {6, 4, 2}]
RESULTS = {}

# helpers
def isDone(pzl, filledPos): # check whether game is finished
    if filledPos < 5: # impossible to finish if < 5 moves
        return False, ''
    for cstr in WINSTR:
        if allXs(pzl, cstr): # if there are 3 X's in a row
            return True, 1 # return that it's done with winner X
        elif allOs(pzl, cstr): # same for O
            return True, -1
    if filledPos == 9: # if there's no X or O winner but board full
        return True, 0 # it's a draw
    return False, ''

def allXs(pzl, cstr): # check for 3 X's in a row, col, or diagonal
    for index in cstr:
        if pzl[index] != 'x':
            return False
    return True

def allOs(pzl, cstr):
    for index in cstr:
        if pzl[index] != 'o':
            return False
    return True

def updateResults(filledPos, pzl, result): # update global results
    if filledPos == 9:                     # to include new finished games
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


# ive got no idea what im doing
def minimax(pzl, filledPos):
    solved, result = isDone(pzl, filledPos)
    if solved:
        return {-1: result}

    moveResults = {}  # {move: board eval}
    possMoves = {index for index, chr in enumerate(pzl) if chr == '.'}  # fix/do better later
    tkn = 'o' if filledPos % 2 else 'x'

    for move in possMoves:
        newPzl = pzl[:move] + tkn + pzl[move + 1:]
        mmx = minimax(newPzl, filledPos + 1)
        brdEval = min(mmx.values()) if tkn == 'x' else max(mmx.values())
        moveResults[move] = brdEval

    return moveResults


# testing
#testPzl = '.' * 9 # no moves made
#testPzl = '.xxooxoxo' # one move away from x win in 9 moves
#testPzl = 'xoxoxxo.o' # one move away from draw in 9 moves
#testPzl = 'xx..oooxx' # one move away from o win in 8 steps
#testPzl = 'x.x.xo.oo' # one move away from x win in 7 steps
#testPzl = 'xo..oxx..' # one move away from o win in 6 steps
#testPzl = 'o.x..xo..' # one move away from x win in 5 steps
#startSteps = 8 # one less than winning steps
#printPzl(testPzl)
#print(minimax(testPzl, startSteps))


# idk input stuff
inp = input('What token? ')
personTkn = inp if inp != '' else 'x'
cptrTkn = 'o' if personTkn == 'x' else 'x'
personMove = 1 if personTkn == 'x' else 0
board = '.' * 9
numMoves = 0

printPzl(board)
print('Your token is: {} Computers token is: {}'.format(personTkn, cptrTkn))

while numMoves != 9: # clean up later

    print('Moves made:', numMoves)

    if numMoves % 2 != personMove:
        move = input('move where? ')
        if move not in '012345678':
            input('Thats not a move. Try again dude. ')
        move = int(move)
        if board[move] != '.':
            input('Thats taken. Move where? ')
        board = makeMove(board, move, personTkn)
        print('You placed {} at index {}: '.format(personTkn, move))
        printPzl(board)
        numMoves += 1
        done, result = isDone(board, numMoves)
        if done:
            output = 'Wow! You just won.' if result == personMove else 'Its a tie :O'
            print(output)
            quit()

    else:
        move = min(minimax(board, numMoves)) if cptrTkn == 'o' \
            else max(minimax(board, numMoves))
        board = makeMove(board, move, cptrTkn)
        print('Computer placed {} at index {}: '.format(cptrTkn, move))
        printPzl(board)
        numMoves += 1
        done, result = isDone(board, numMoves)
        if done:
            print('Wow! You just lost. That sucks.')
            quit()
