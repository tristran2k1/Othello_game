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

    you = lines[12]
    return minimax_decision(victory_cell, cell, you)

def heuristic(cell, whoseTurn, victory_cell,current_cell) :                    #add victory_cell, cell_currently
    opponent = 'B' if whoseTurn == 'W' else 'W'
    ourScore, opponentScore = cell.getResultEdge(victory_cell)          #sai teen

    return ourScore - opponentScore
def minimax_decision(victory_cells,cell,you) :
    game_ai = Game()
    game_ai.addInfor(victory_cells,cell)

    whoseTurn = 'B' if you == "BLACK" else 'W'
    opponent = 'W'if whoseTurn =='B' else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, whoseTurn):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:
        #remember the best move
        best_move_val = -99999
        best_location = possible_positions[0]

        #Try out every single move
        for i in range(len(possible_positions)):
            #temp_cell = Board()
            temp_cell= cell.copy()
            temp_cell.place(possible_positions[i],whoseTurn)
            val = minimaxValue(temp_cell,whoseTurn,opponent,0,game_ai,possible_positions[i])  #add possible_position[i]
            if best_move_val < val:
                best_move_val = val
                best_location = possible_positions[i]
        return best_location
    else :
        return "NULL"
def minimaxValue(cell,originalTurn, currentTurn,searchPly,game_ai,current_position):
    if searchPly == 10 or game_ai.checkGameOver() == True:
        return heuristic(cell,originalTurn,game_ai.getVictoryCell(),current_position)
    opponent = 'W' if currentTurn == 'B' else 'W'

    possible_positions = []
    for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
        if cell.isPlaceable(c + r, currentTurn):
            possible_positions.append(c + r)

    if len(possible_positions) > 0:
        return minimaxValue(cell,originalTurn,opponent,searchPly+1,game_ai,current_position)
    else:
        #remember the best move
        best_move_val = -99999
        if originalTurn != currentTurn:
            best_move_val = 99999

        #Try out every single move
        for i in range(len(possible_positions)):
            #apply the new board
            temp_cell = cell.copy()
            temp_cell.place(possible_positions[i],currentTurn)
            #recursive call
            val = minimaxValue(temp_cell,originalTurn,opponent,searchPly+1,game_ai,possible_positions[i])
            #remember best move
            if originalTurn == currentTurn:
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














