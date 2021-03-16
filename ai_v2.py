import itertools
from init import *
import copy

cached = {} #STATE : UTILITY

def compute_utility(board, color):

    black_score , white_score = board.getResult()

    if color =='B':
        return black_score - white_score
    else:
        return white_score - black_score

############ MINIMAX ###############################
#MAX = 1
#MIN = 2
def minimax_min_node(board, color): #returns lowest attainable utility
    if color == 'W':
        opponent = 'B'
    else:
        opponent = 'W'

    if board in cached:
        return cached[board]

    if not board.get_possible_moves(color):
        return compute_utility(board,color)

    v = float("Inf")
    temp_board = Board()
    temp_board = board.copy()
    for move in board.get_possible_moves(color):

        v = min(v,minimax_min_node(temp_board.place(move,color),opponent))
    return v

def minimax_max_node(board,color):
    if color == 'W':
        opponent = 'B'
    else:
        opponent = 'W'

    if board in cached:
        return cached[board]

    if not board.get_possible_moves(color):
        return compute_utility(board,color)

    v = float("-Inf")

    temp_board = board.copy()
    for move in board.get_possible_moves(color):
        v = max(v,minimax_min_node(temp_board.place(move,color),opponent))
    return v

def select_move_minimax(board,color):
    moves = []

    for option in board.get_possible_moves(color): #get all minimizer moves
        temp_board = board.copy()
        new_move = temp_board.place(option,color)
        utility  = minimax_max_node(new_move,color)
        if new_move not in cached:
            cached[new_move] = utility
        moves.append([option,utility])
    sorted_option = sorted(moves,key=lambda x:x[1])
    return sorted_option[0][0]

def callBot_ai(game_info):
    lines = game_info.split('\n')

    victory_cell = lines[1].split(' ')

    cell = Board()
    cell.update(lines[3:11])

    you = lines[12]         ###you ----> color
    return select_move_minimax(cell,you)