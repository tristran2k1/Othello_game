import itertools
from typing import List

import numpy as np

def ip():
    return "172.16.5.181"
class Board:
    def __init__(self):
        self.victoryCell = []
        self.whoseTurn = 'B'
        self.data = np.array([['E'] * 8] * 8)
        self.data[3, 3] = self.data[4, 4] = 'W'
        self.data[3, 4] = self.data[4, 3] = 'B'


    # numeric_character: "12345678"
    # return: index of row
    def getRowId(self, numeric_character):
        return ord(numeric_character) - ord('1')

    # numeric_character: "12345678"
    # return: values of row
    def getRow(self, numeric_character):
        return self.data[self.getRowId(numeric_character), :]

    # alphabet_character: "abcdefgh"
    # return: index of column
    def getColumnId(self, alphabet_character):
        return ord(alphabet_character) - ord('a')

    # alphabet_character: "abcdefgh"
    # return: values of column
    def getColumn(self, alphabet_character):
        return self.data[:, self.getColumnId(alphabet_character)]

    # position: "^\w\d$"
    # return: value at position
    def getValue(self, position):
        alphabet_character, numeric_character = tuple(position)
        return self.data[self.getRowId(numeric_character),
                         self.getColumnId(alphabet_character)]

    # r, c: int
    # return: {True, False}
    def isOutOfRange(self, r, c):
        return (r < 0) or (r > 7) or (c < 0) or (c > 7)

    # position: "^\w\d$"
    # direction: (int, int) ~ (r, c)
    # color: {'B', 'W'}
    # return: {True, False}
    def isDirectionPlaceable(self, position, direction, color):
        if self.getValue(position) != 'E':
            return False

        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)
        row_direction, column_direction = direction

        for i in range(1, 9):
            r = row_id + i * row_direction
            c = column_id + i * column_direction
            if self.isOutOfRange(r, c) or (self.data[r, c] == 'E'):
                return False
            if self.data[r, c] == color:
                if i == 1:
                    return False
                else:
                    return True

    # position: "^\w\d$"
    # color: {'B', 'W'}
    # return: {True, False}
    def isPlaceable(self, position, color):
        return self.isDirectionPlaceable(position, ( 1,  0), color) or    \
               self.isDirectionPlaceable(position, ( 1,  1), color) or    \
               self.isDirectionPlaceable(position, ( 0,  1), color) or    \
               self.isDirectionPlaceable(position, (-1,  1), color) or    \
               self.isDirectionPlaceable(position, (-1,  0), color) or    \
               self.isDirectionPlaceable(position, (-1, -1), color) or    \
               self.isDirectionPlaceable(position, ( 0, -1), color) or    \
               self.isDirectionPlaceable(position, ( 1, -1), color)

    # color: {'B', 'W'}
    # return: {True, False}
    def isPlayable(self, color):
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if self.isPlaceable(c + r, color):
                return True
        return False

    # return: (int, int) ~ (b, w)
    def getResult(self):
        b, w = 0, 0
        for (r, c) in itertools.product(range(8), range(8)):
            b += 1 if self.data[r, c] == 'B' else 0
            w += 1 if self.data[r, c] == 'W' else 0
        return b, w

    # return: (int, int) ~ (b, w)
    def getResultEdge(self):
        b, w = 0, 0
        v_b, v_w =0, 0
        for (r, c) in itertools.product(range(8), range(8)):
            if self.data[r, c] == 'B':
                if self.isCorner(self.data[r, c]):
                    b += 50
                if self.isEdge(self.data[r, c]):
                    b += 20
                if isVictory_cell(self.victoryCell, self.data[r, c]):
                    v_b += 1
                    b += 30
                else:
                    b += 1
            if self.data[r, c] == 'W':
                if self.isCorner(self.data[r, c]):
                    w += 50
                if self.isEdge(self.data[r, c]):
                    w += 20
                if isVictory_cell(self.victoryCell, self.data[r, c]):
                    v_w += 1
                    w += 30
                else:
                    w+=1
        tempBoard = Board()
        tempBoard = self.copy()
        tmpX = []
        tmpY = []
        numMovesA = tempBoard.getMoveList(tmpX,tmpY)
        tempBoard.setCurrentPlayer(tempBoard.getOpponentPiece())

        numMovesB = tempBoard.getMoveList(tmpX,tmpY)
        if self.getWhosePiece() == 'B':#white is no change
            tmp = numMovesB
            numMovesB = numMovesA
            numMovesA = tmp
        #white = numMovesA, black = numMovesB
        if numMovesA == 0 and numMovesB != 0:
            w = -99999
        elif numMovesB == 0 and numMovesA != 0:
            b = -99999
        if v_b == 5:
            b = 99999
        elif v_w ==5:
            w = 99999
        return b, w


    # position: "^\w\d$"
    # direction: (int, int) ~ (r, c)
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def getDirectionFlips(self, position, direction, color):
        if self.getValue(position) != 'E':
            return []

        ret = []
        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)
        row_direction, column_direction = direction

        for i in range(1, 9):
            r = row_id + i * row_direction
            c = column_id + i * column_direction
            if (r < 0) or (r > 7) or (c < 0) or (c > 7) or (self.data[r, c] == 'E'):
                return []
            if self.data[r, c] == color:
                return ret
            ret.append((r, c))

    # position: "^\w\d$"
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def getFlips(self, position, color):
        return self.getDirectionFlips(position, ( 1,  0), color) +    \
               self.getDirectionFlips(position, ( 1,  1), color) +    \
               self.getDirectionFlips(position, ( 0,  1), color) +    \
               self.getDirectionFlips(position, (-1,  1), color) +    \
               self.getDirectionFlips(position, (-1,  0), color) +    \
               self.getDirectionFlips(position, (-1, -1), color) +    \
               self.getDirectionFlips(position, ( 0, -1), color) +    \
               self.getDirectionFlips(position, ( 1, -1), color)

    # Assume that the 'color' player can place a piece at the 'position' cell of the board
    # color: {'B', 'W'}
    # return: list of cells which will change color
    def place(self, position, color):
        alphabet_character, numeric_character = tuple(position)
        row_id = self.getRowId(numeric_character)
        column_id = self.getColumnId(alphabet_character)

        changing_cells = self.getFlips(position, color) + [(row_id, column_id)]
        for (r, c) in changing_cells:
            self.data[r, c] = color
        return self.data

    # cell_lines: only lines of the 'cell' variable in the string which
    #             is returned by Game.getInfo function
    def update(self, cell_lines):
        for r in range(8):
            cells = cell_lines[r].split(' ')
            for c in range(8):
                self.data[r, c] = cells[c]

    def isCorner(self,position):
        return True if position in {'a1','a8','h1','h8'} else False

    def isEdge(self,position):
        return True if position in {'a1','a2','a3','a4','a5','a6','a7','a8',
                                    'b1','c1','d1','e1','f1','g1','h1'} \
            else False

    def copy(self):
        obj = Board()
        obj.data = self.data.copy()
        obj.victoryCell = self.victoryCell
        obj.whoseTurn = self.whoseTurn
        return obj

    def move_(self):
        self.data[1,3]='W'

    def find_lines(board, i, j, player):
        """
        Find all the uninterupted lines of stones that would be captured if player
        plays column i and row j.
        """
        lines = []
        for xdir, ydir in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1],
                           [-1, 0], [-1, 1]]:
            u = i
            v = j
            line = []

            u += xdir
            v += ydir
            found = False
            while 0 <= u < len(board) and 0 <= v < len(board):
                if board[v][u] == 0:
                    break
                elif board[v][u] == player:
                    found = True
                    break
                else:
                    line.append((u, v))
                u += xdir
                v += ydir
            if found and line:
                lines.append(line)
        return lines

    def play_move(board, player, i, j):
        new_board = []
        for row in board:
            new_board.append(list(row[:]))
        lines = board.find_lines(board, i, j, player)
        new_board[j][i] = player
        for line in lines:
            for u, v in line:
                new_board[v][u] = player
        final = []
        for row in new_board:
            final.append(tuple(row))
        return tuple(final)

    def get_possible_moves(self,color):
        possible_positions = []
        for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
            if self.isPlaceable(c + r, color):
                possible_positions.append(c + r)
        return possible_positions

    ###ADD
    def setVictoryCell(self,victoryCell):
        self.victoryCell = victoryCell

    #Checks a direction from x, y to see if we can make a move
    def checkFlip(self, x, y, deltaX, deltaY):
        if (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
            opponentPiece = self.getOpponentPiece()
            myPiece = self.whoseTurn

            if self.data[x][y] == opponentPiece:
                while (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
                    x += deltaX
                    y += deltaY

                    if (x >= 0) and (x < 8) and (y >= 0) and (y < 8):
                        if self.data[x][y] == 'E':
                            return False
                        if self.data[x][y] == myPiece:
                            return True
                        else:
                            # It is an opponent piece, just keep scanning in our direction
                            continue
            return False
        return False

    def flipPieces(self,x,y,deltaX,deltaY):

        while  ((x >= 0) and (x < 8) and (y >= 0) and (y < 8)) and (self.data[x][y] == self.getOpponentPiece()):
            self.data[x][y] = self.whoseTurn
            x += deltaX
            y += deltaX

    def getWhosePiece(self):
        return self.whoseTurn

    def getOpponentPiece(self):
        if self.whoseTurn == 'B':
            return 'W'
        return 'B'

    def setCurrentPlayer(self, player):
        self.whoseTurn = player
    #def display(self):

    def makeMove(self,x,y):
        self.data[x][y] = self.whoseTurn

        #check to the left
        if self.checkFlip(x - 1, y, -1, 0):
            self.flipPieces(x - 1, y, -1, 0)
        #check to the right
        if self.checkFlip(x + 1, y, 1, 0):
            self.flipPieces(x + 1, y, 1, 0)
        # check down
        if self.checkFlip(x, y-1, 0, -1):
            self.flipPieces(x , y-1, 0, -1)
        # check up
        if self.checkFlip(x, y + 1, 0, 1):
            self.flipPieces(x, y + 1, 0, 1)
        #Check down - left
        if self.checkFlip(x - 1, y - 1, -1, -1):
            self.flipPieces(x - 1, y - 1, -1, -1)
        #Check down - right
        if self.checkFlip(x + 1, y - 1, 1, -1):
            self.flipPieces(x + 1, y - 1, 1, -1)
        #Check up - left
        if self.checkFlip(x - 1, y + 1, -1, 1):
            self.flipPieces(x - 1, y + 1, -1, 1)
        #Check up - right
        if self.checkFlip(x + 1, y + 1, 1, 1):
            self.flipPieces(x + 1, y + 1, 1, 1)

    def validMove(self,x,y):
        #Check that the coordinates are empty
        if self.data[x][y] != 'E':
            return False
        #If we can flip in any direction, it is valid
        #Check to the left
        if self.checkFlip(x - 1, y, -1, 0):
            return True
        #Check to the right
        if self.checkFlip(x + 1, y, 1, 0):
            return True
        #Check down
        if self.checkFlip(x, y - 1, 0, -1):
            return True
        #Check up
        if self.checkFlip(x, y + 1, 0, 1):
            return True
        #Check down - left
        if self.checkFlip(x - 1, y - 1, -1, -1):
            return True
        #Check down - right
        if self.checkFlip(x + 1, y - 1, 1, -1):
            return True
        #Check up - left
        if self.checkFlip(x - 1, y + 1, -1, 1):
            return True
        #Check up - right
        if self.checkFlip(x + 1, y + 1, 1, 1):
            return True

        return False #If we get here, we didn't find a valid flip direction

    def getMoveList(self, moveX, moveY):
        numMove = 0
        for x in range(8):
            for y in range(8):
                if self.validMove(x, y):
                    moveX.append(x)
                    moveY.append(y)
                    numMove+=1

        return numMove

    #True if the game is over, false if not over
    def gameOver(self):
        XMoveX = []
        XMoveY = []
        OMoveX = []
        OMoveY = []

        numXMoves = self.getMoveList(XMoveX,XMoveY)
        #Temporarily flip whoseturn to opponent to get opponent move list
        whoseTurn = self.getOpponentPiece()
        numOMoves = self.getMoveList(OMoveX,OMoveY)
        whoseTurn = self.getOpponentPiece() #Flip back to original

        if numXMoves == 0 and numOMoves == 0:
            return True
        return False

    def heuristic(self, whoseTurn):  # add victory_cell, cell_currently
        ourScore, opponentScore = self.getResultEdge()  # sai teen
        if whoseTurn =='B':
            return ourScore - opponentScore
        else:
            return opponentScore - ourScore

    def getData(self):
        return self.data

    def numalpha_To_Numnum(self):
        victory_numnum = np.array([[0] * len(self.victoryCell)] * 2)
        for i in range(len(self.victoryCell)):
            alphabet_character, numeric_character = tuple(self.victoryCell[i])
            row_id = self.getRowId(numeric_character)
            column_id = self.getColumnId(alphabet_character)
            victory_numnum[0][i] = row_id
            victory_numnum[1][i] = column_id
        return victory_numnum

class Game:
    def __init__(self):
        random_numbers = np.random.choice(64, 5, replace = False)
        self.victory_cells = [chr(x // 8 + ord('a')) + chr(x % 8 + ord('1')) for x in random_numbers]
        self.board = Board()
        self.history = []
        self.winner = None

    # return: {"BLACK", "WHITE"} ~ who will play next
    def getNextTurn(self):
        return "BLACK" if len(self.history) % 2 == 0 else "WHITE"

    # return: {True, False} ~ check if the game is over
    def checkGameOver(self):
        if self.winner is not None:
            return True

        v_b, v_w = 0, 0
        for cell in self.victory_cells:
            v_b += 1 if self.board.getValue(cell) == 'B' else 0
            v_w += 1 if self.board.getValue(cell) == 'W' else 0
        if v_b == 5:
            self.winner = "BLACK"
            return True
        if v_w == 5:
            self.winner = "WHITE"
            return True

        color = 'B' if self.getNextTurn() == "BLACK" else 'W'
        if not self.board.isPlayable(color):
            b, w = self.board.getResult()
            self.winner = "BLACK" if b > w else self.winner
            self.winner = "WHITE" if b < w else self.winner
            if b == w:
                self.winner = "BLACK" if v_b > v_w else self.winner
                self.winner = "WHITE" if v_b < v_w else self.winner
                self.winner = "DRAW" if v_b == v_w else self.winner
            return True
        return False

    def setNextTurn(self, position):
        if self.checkGameOver():
            return False

        if position == "NULL":
            self.winner = "WHITE" if self.getNextTurn() == "BLACK" else 'BLACK'
            return True

        color = 'B' if self.getNextTurn() == "BLACK" else 'W'

        if not self.board.isPlaceable(position, color):
            return False

        self.board.place(position, color)
        self.history.append(position)
        self.checkGameOver()
        return True

    def getWinner(self):
        return self.winner

    def getInfo(self):
        s = ""

        s += "victory_cell\n"
        s += " ".join(self.victory_cells) + "\n"

        s += "cell\n"
        s += "\n".join(" ".join(self.board.getRow(r)) for r in "12345678") + "\n"

        s += "you\n"
        s += self.getNextTurn() + "\n"

        return s

    def getFinalResult(self):

        s = ""

        if not self.checkGameOver():
            return s
        s += self.getInfo()
        s += "history\n"
        s += " ".join(self.history) + "\n"

        s += "winner\n"
        s += self.getWinner() + "\n"
        b,w = self.board.getResult()

        s +="Black: "
        s+=str(b)
        s+="White"
        s+=str(w)

        return s

    def addInfor(self,victory,cells):
        self.victory_cells = victory
        self.board = cells.copy()

    def getVictoryCell(self):
        return self.victory_cells

def isVictory_cell(victory_cell,position):
    return True if position in victory_cell else False






