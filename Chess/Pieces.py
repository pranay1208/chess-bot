WHITE = "white"
BLACK = "black"
chessCardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chessDiagonals = [(1, 1), (-1, 1), (1, -1), (-1, -1)]


class Piece:
    def __init__(self, color=None):
        self.Color = color

    def isValid(self, startpos, endpos, Color, board):
        if endpos in self.availableMoves(startpos[0], startpos[1], board, Color=Color):
            return True
        return False

    def availableMoves(self, x, y, gameboard, Color=None):
        print("ERROR: no movement for base class")

    def isInBounds(self, x, y):
        "checks if a position is on the board"
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return True
        return False

    def noConflict(self, board, initialColor, x, y):
        "checks if a single position poses no conflict to the rules of chess"
        if self.isInBounds(x, y) and ((board.getPiece(x, y) is None or board.getPiece(x, y).Color != initialColor)):
            return True
        return False

    def AdNauseum(self, x, y, board, Color, intervals):
        """repeats the given interval until another piece is run into. 
        if that piece is not of the same color, that square is added and
         then the list is returned"""
        answers = []
        for xint, yint in intervals:
            xtemp, ytemp = x+xint, y+yint
            while self.isInBounds(xtemp, ytemp):
                #print(str((xtemp,ytemp))+"is in bounds")
                target = board.getPiece(xtemp, ytemp)
                if target is None:
                    answers.append((xtemp, ytemp))
                elif target.Color != Color:
                    answers.append((xtemp, ytemp))
                    break
                else:
                    break
                xtemp, ytemp = xtemp + xint, ytemp + yint
        return answers


class Knight(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♘'
        return '♞'

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        return [(xx, yy) for xx, yy in self.knightList(x, y, 2, 1) if self.noConflict(board, Color, xx, yy)]

    def knightList(self, x, y, int1, int2):
        # specifically for the knight, permutes the values needed around a position for noConflict tests
        return [(x+int1, y+int2), (x-int1, y+int2), (x+int1, y-int2), (x-int1, y-int2), (x+int2, y+int1), (x-int2, y+int1), (x+int2, y-int1), (x-int2, y-int1)]


class Rook(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♖'
        return '♜'

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        return self.AdNauseum(x, y, board, Color, chessCardinals)


class Bishop(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♗'
        return '♝'

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        return self.AdNauseum(x, y, board, Color, chessDiagonals)


class Queen(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♕'
        return '♛'

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        return self.AdNauseum(x, y, board, Color, chessCardinals+chessDiagonals)


class King(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♔'
        return '♚'

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        return [(xx, yy) for xx, yy in self.kingList(x, y) if self.noConflict(board, Color, xx, yy)]

    def kingList(self, x, y):
        return [(x+1, y), (x+1, y+1), (x+1, y-1), (x, y+1), (x, y-1), (x-1, y), (x-1, y+1), (x-1, y-1)]


class Pawn(Piece):
    def __str__(self) -> str:
        if self.Color == WHITE:
            return '♙'
        return '♟'

    def __init__(self, Color) -> None:
        super().__init__(Color)
        self.direction = 0
        if Color == WHITE:
            self.direction = 1
        else:
            self.direction = -1

    def availableMoves(self, x, y, board, Color=None):
        if Color is None:
            Color = self.Color
        moves = []
        if self.noConflict(board, Color, x+1, y+self.direction) and board.getPiece(x+1, y+self.direction) is not None:
            moves.append((x+1, y+self.direction))
        if self.noConflict(board, Color, x-1, y+self.direction) and board.getPiece(x-1, y+self.direction) is not None:
            moves.append((x-1, y+self.direction))

        if self.noConflict(board, Color, x, y+self.direction) and board.getPiece(x, y+self.direction) is None:
            moves.append((x, y+self.direction))
            if (y == 1 or y == 6) and self.noConflict(board, Color, x, y+2*self.direction) and board.getPiece(x, y+2*self.direction) is None:
                moves.append((x, y+2*self.direction))

        return moves
