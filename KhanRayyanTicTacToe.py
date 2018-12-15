import msvcrt
import sys


# tic tac toe final 12-5-18
# due 12-6-18


# helpers
def isDone(pzl, filledPos):  # check whether game is finished

    winstr = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8}, {0, 3, 6},
              {1, 4, 7}, {2, 5, 8}, {0, 4, 8}, {6, 4, 2}]
    # rows, columns, and diagonals to fill to win

    if filledPos < 5:  # impossible to finish if < 5 moves
        return False, 0
    for cstr in winstr:
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


def allOs(pzl, cstr):  # same as above
    for index in cstr:
        if pzl[index] != 'o':
            return False
    return True


# sort moves by good, bad, draw
def categorizeMoves(pzl):
    if pzl == '.' * 9:
        return set(), set(), {4, 0, 2, 6, 8, 1, 3, 5, 7}

    currentPlayer = 'x' if pzl.count('.') % 2 else 'o'  # determine current token
    solved, result = isDone(pzl, 9 - pzl.count('.'))  # if you're at the end
    if solved:
        # return {good}, {bad}, {draw} based on token/outcome
        if result == -1 and currentPlayer == 'x':  # -1 means O win, bad for X
            return set(), {-1}, set()  # therefore gets put in its 'bad' set
        elif result == 1 and currentPlayer == 'x':
            return {-1}, set(), set()
        elif result == 0:  # if its a draw, it goes there regardless of player
            return set(), set(), {-1}
        elif result == -1 and currentPlayer == 'o':  # vice-versa from above
            return {-1}, set(), set()
        elif result == 1 and currentPlayer == 'o':
            return set(), {-1}, set()

    good, bad, tie = set(), set(), set()
    # if you're not solved, generate good/bad/draw

    possMoves = {index for index, chr in
                 enumerate(pzl) if chr == '.'}  # fix/do better later -- nvm lazy
    # find empty indexes

    for move in possMoves:  # check results of move into each open index
        newPzl = pzl[:move] + currentPlayer + pzl[move + 1:]

        oppGood, oppBad, oppTie = categorizeMoves(newPzl)
        # since you're one move up, that means you're getting the
        # results for the OPPOSITE side -- what's good for them
        # is bad for the current move

        if oppGood:  # if there's anything good for the opposite side
            bad.add(move)  # add it to this side's set of bad moves
        elif oppTie:
            tie.add(move)
        else:  # vice-versa for oppBad
            good.add(move)

    return good, bad, tie


# play + its helper methods (alphabetical):

def checkExit(inp):
    if ord(inp) == 27:  # if its the 'esc' key
        exit('Game ended.')  # end the game
    return inp  # otherwise carry on


def getInp(prompt):
    if len(sys.argv) == 2:  # if it got a second input
        inpt = sys.argv[1].lower()
        if len(inpt) == 1 and inpt in 'xo': # if its a token, return it
            return inpt
        elif len(inpt) != 9:  # check if its actually a board
            print('Input wasn\'t the size of a tic-tac-toe board.')
        elif {ch for ch in inpt} != {'.', 'o', 'x'} \
                and {ch for ch in inpt} != {'.', 'o'} \
                and {ch for ch in inpt} != {'.', 'x'} \
                and {ch for ch in inpt} != {'.'}:
            # to future self if you read this: i'm sorry for this if-statement
            # at least it'll be funny though
            print('Input wasn\'t a board -- character besides x, o, or \'.\'')

        elif inpt.count('o') > sys.argv[1].count('x'):
            print('Input wasn\'t a legal board (more o\'s than x\'s).')

        else:
            return inpt  # if it is, return it

    print(prompt)  # otherwise request a move
    tkn = str(checkExit(msvcrt.getch()))
    return tkn.lower()
    # check if it's an 'esc' otherwise return it


def getMove(prompt, board):  # gets the player's next move
    print(prompt)  # prompts player for move
    while True:
        inp = str(checkExit(msvcrt.getch()))  # checks input for exit
        if inp[2] not in '012345678':  # if its not a possible index
            print('That\'s not a move. Try again.')  # request a new one
            continue
        inp = int(inp[2])
        if board[inp] != '.':  # if it's a filled space
            print('That\'s taken. Move where?')  # request a new one
            continue
        return inp  # you get out of the while-loop when you have a valid move


def getNextToken(pzl):  # used by startVals method if given a board
    if pzl.count('.') % 2:
        return 'x'
    return 'o'


def getPredictions(good, bad, tie):
    # just formats the sets into a nice string to print

    predictions = 'W: (' + ', '.join \
        ([str(i) for i in good]) if good else 'W: (none'
    predictions += ') L: (' + ', '.join \
        ([str(i) for i in bad]) if bad else ') L: (none'
    predictions += ') T: (' + ', '.join \
        ([str(i) for i in tie]) + ')' if tie else ') T: (none)'
    return predictions


def makeMove(pzl, moveIndex, token):
    return pzl[:moveIndex] + token + pzl[moveIndex + 1:]


def setStartVals(inp):
    # sets below variables based on input of either a partially
    # completed board or an 'x' or 'o' token
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
    # returns either board or token or exits if 'esc' pressed

    personTkn, cptrTkn, personTurn, board, numMoves \
        = setStartVals(inp)
    # given either the board or token, determine the person's
    # or computer's token, 1 or 0 for when it's the person's turn,
    # board (empty if not given), and number of moves made so far

    print('Your token is: {} Computer\'s token is: {}'
          .format(personTkn, cptrTkn))
    printPzl(board)

    while True:  # keep making moves until the game finishes and exits
        if msvcrt.kbhit():  # if a key's been pressed w/o a getMove prompt
            checkExit(msvcrt.getch())  # check if its esc, if so end game

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
            good, bad, tie = categorizeMoves(board)  # get categorized moves
            move = [*good, *tie, *bad][0]  # order best-worst, get first
            predictions = getPredictions(good, bad, tie)  # just for printing
            board = makeMove(board, move, cptrTkn)  # update board
            print('Computer placed {} at index {} of choices: {}'
                  .format(cptrTkn, move, predictions))
            printPzl(board)
            numMoves += 1
            done, result = isDone(board, numMoves)  # check whether game is done
            if done:
                output = 'Wow! You just lost. That sucks.' \
                    if result != 0 * personTurn else 'It\'s a tie :O'
                exit(output)


play()
