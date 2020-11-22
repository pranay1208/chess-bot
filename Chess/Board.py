from math import pi
from .Pieces import *
from .Pieces import WHITE as W, BLACK as B

WHITE = W
BLACK = B


class Board:
    def __init__(self, board=None):
        if board is None:
            self.readyPosition()
        else:
            self.gameboard = []
            for row in board:
                gameRow = []
                for piece in row:
                    gameRow.append(piece)
                self.gameboard.append(gameRow)

    def readyPosition(self):
        self.gameboard = [
            [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
             King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
            [Pawn(WHITE) for _ in range(8)],
        ]
        for _ in range(4):
            self.gameboard.append([None for _ in range(8)])
        self.gameboard.extend([
            [Pawn(BLACK) for _ in range(8)],
            [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
             King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]])

    def __str__(self):
        toReturn = ""
        for index in range(len(self.gameboard), 0, -1):
            row = self.gameboard[index-1]
            toReturn += str(index)+" "
            for piece in row:
                printPiece = piece
                if(piece is None):
                    printPiece = '.'
                toReturn += str(printPiece) + " "
            toReturn += "\n"
        return toReturn + "  a b c d e f g h"

    def getPiece(self, x, y) -> Piece:
        return self.gameboard[y][x]

    def setPiece(self, x, y, piece):
        self.gameboard[y][x] = piece

    def movePiece(self, startPos, endPos, piece):
        self.setPiece(*endPos, piece)
        self.setPiece(*startPos, None)

    # The color indicates who is giving check
    def isChecked(self, Color):
        oppKing = "♚" if Color == WHITE else "♔"
        kingPosition = ()
        for y in range(len(self.gameboard)):
            for x in range(len(self.gameboard[y])):
                if str(self.getPiece(x, y)) == oppKing:
                    kingPosition = (x, y)
                    break

        for y in range(len(self.gameboard)):
            for x in range(len(self.gameboard[y])):
                piece = self.getPiece(x, y)
                if piece is None or piece.Color != Color:
                    continue
                if self.canAttackKing(x, y, piece, kingPosition, Color):
                    return True
        return False

    def canAttackKing(self, x, y,  piece, kingPosition, selfColor):
        return piece.isValid((x, y), kingPosition, selfColor, self)
