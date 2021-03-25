import itertools, random
from init import *
from gui import GUI


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

# Initial values of Alpha and Beta
MAX, MIN = 1000, -1000

def callBot_ai(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')
    cell = Board()

    cell.update(lines[3:11])

    cell.setVictoryCell(victory_cell)
    alpha = GUI(cell.getData(),cell.numalpha_To_Numnum())
    alpha.drawVictoryCell()
    if "winner" in game_info:
        winner = lines[16]
    else:
        winner = None
    alpha.run(winner)
    if lines[12] == "WHITE":
        cell.setCurrentPlayer('W')
    else :
        cell.setCurrentPlayer('B')
    alpha.run(winner)
    x,y = minimax_decision(cell)

    if x == -1:
        result = "NULL"
    else:
        x = x + 1
        alphabet_col = ['a','b','c','d','e','f','g','h']
        result = str(alphabet_col[y])+str(x)
    cell.makeMove(x-1, y)
    alpha = GUI(cell.getData(),cell.numalpha_To_Numnum())
    alpha.drawVictoryCell()
    alpha.run(winner)
    return result

def minimax_decision(board) :
    moveX = []
    moveY = []
    opponent = board.getOpponentPiece()
    numMoves = board.getMoveList(moveX,moveY)
    #print(numMoves)
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
        val = minimaxValueAlphaBeta(tempBoard,board.getWhosePiece(),1,MIN,MAX)

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

def minimaxValueAlphaBeta(board, originalTurn, searchPly, beta, alpha):
    if (searchPly == 30 ) or board.gameOver(): # Change to desired ply lookahead
        return board.heuristic(originalTurn) # Termination criteria

    moveX = []
    moveY = []
    opponent = board.getOpponentPiece()

    numMoves = board.getMoveList(moveX, moveY)
    if numMoves == 0:#if no moves skip to next player's turn
        tempBoard = Board()
        tempBoard = board.copy()
        tempBoard.setCurrentPlayer(opponent)
        return minimaxValueAlphaBeta(tempBoard, originalTurn, searchPly + 1, beta, alpha);
    else:
        bestMoveVal = -99999
        if originalTurn != board.getWhosePiece():
            bestMoveVal = 99999 # for finding min
        for i in range(numMoves):
            # Apply the move to a new board
            tempBoard = Board()
            tempBoard = board.copy()
            tempBoard.makeMove(moveX[i], moveY[i])
            #Recursive call
            #Opponent 's turn
            tempBoard.setCurrentPlayer(tempBoard.getOpponentPiece())
            val = minimaxValueAlphaBeta(tempBoard, originalTurn, searchPly + 1, beta, alpha)
            #Remember best move
            if originalTurn == board.getWhosePiece():
                # Remember max if it 's the originator' s turn
                if val > bestMoveVal:
                    bestMoveVal = val
                if bestMoveVal >= alpha:
                    alpha = bestMoveVal
                if alpha >= beta:
                    break
            else:
                if val < bestMoveVal:
                    bestMoveVal = val
                if bestMoveVal <= beta:
                    beta = bestMoveVal
                if alpha >= beta:
                    break
        return bestMoveVal
