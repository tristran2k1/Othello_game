import itertools, random

from init import *
import copy
def bot(victory_cell, cell, you):
    color = 'B' if you == "BLACK" else 'W'

    posible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, color):
            posible_positions.append(c + r)

    if len(posible_positions) > 0:
        return random.choice(posible_positions)
    else:
        return "NULL"
def callBot(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]
    return bot(victory_cell, cell, you)


def callBot_ai(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    #you = lines[12]

    cell.setVictoryCell(victory_cell)
    cell.setCurrentPlayer('W')
    x,y = minimax_decision(cell)

    if x == -1:
        return "NULL"
    else:
        x = x + 1
        alphabet_col = ['a','b','c','d','e','f','g','h']
        result = str(alphabet_col[y])+str(x)
        return result


def minimax_decision(board) :
    moveX = []
    moveY = []
    opponent = board.getOpponentPiece()
    numMoves = board.getMoveList(moveX,moveY)
    print(numMoves)
    if numMoves == 0:
        x = -1
        y = -1
        return x,y

    bestMoveVal = -99999
    bestX = moveX[0]
    bestY = moveY[0]

    for i in range (numMoves):
        tempBoard = Board()
        tempBoard = board.copy()
        tempBoard.makeMove(moveX[i],moveY[i])
        tempBoard.setCurrentPlayer(tempBoard.getOpponentPiece())
        val = minimaxValue(tempBoard,board.getWhosePiece(),1)

        if val > bestMoveVal:
            bestMoveVal = val
            bestX = moveX[i]
            bestY = moveY[i]
    return bestX, bestY

def minimaxValue(board, originalTurn, searchPly):
    if searchPly == 2 or board.gameOver() == True:
        return board.heuristic(originalTurn)

    moveX = []
    moveY = []
    opponent = board.getOpponentPiece()
    numMoves = board.getMoveList(moveX,moveY)

    if numMoves == 0:
        tempBoard = Board()
        tempBoard = board.copy()
        tempBoard.setCurrentPlayer(opponent)
        return minimaxValue(tempBoard,originalTurn, searchPly + 1)
    else:
        #remember the best move
        best_move_val = -99999
        if originalTurn != board.getWhosePiece():
            best_move_val = 99999

        #Try out every single move
        for i in range (numMoves):
            tempBoard = Board()
            tempBoard = board.copy()
            tempBoard.makeMove(moveX[i],moveY[i])
            tempBoard.setCurrentPlayer(tempBoard.getOpponentPiece())
            #recursive call
            val = minimaxValue(tempBoard,originalTurn,searchPly+1)
            #remember best move
            if originalTurn == board.getWhosePiece():
                if val > best_move_val:
                    best_move_val = val
            else :
                if val < best_move_val:
                    best_move_val = val

        return best_move_val


# Python3 program to demonstrate
# working of Alpha-Beta Pruning

# Initial values of Aplha and Beta
MAX, MIN = 1000, -1000


# Returns optimal value for current player
# (Initially called for root and maximizer)
def minimax(depth, nodeIndex, maximizingPlayer,
            values, alpha, beta):
    # Terminating condition. i.e
    # leaf node is reached
    if depth == 3:
        return values[nodeIndex]

    if maximizingPlayer:

        best = MIN

        # Recur for left and right children
        for i in range(0, 2):

            val = minimax(depth + 1, nodeIndex * 2 + i,
                          False, values, alpha, beta)
            best = max(best, val)
            alpha = max(alpha, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best

    else:
        best = MAX

        # Recur for left and
        # right children
        for i in range(0, 2):

            val = minimax(depth + 1, nodeIndex * 2 + i,
                          True, values, alpha, beta)
            best = min(best, val)
            beta = min(beta, best)

            # Alpha Beta Pruning
            if beta <= alpha:
                break

        return best

    # Driver Code














