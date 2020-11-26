from Chess.helperFunctions import parsePositon
from .Board import Board
from .Pieces import *
from .helperFunctions import *

CHECKMATE = "checkmate"
STALEMATE = "stalemate"
GAME = "game"


class Move:
    def __init__(self, start, end, piece):
        self.startPosition = start
        self.endPosition = end
        self.piece = piece

    def __str__(self) -> str:
        return f'{coordToPosition(self.startPosition)} {coordToPosition(self.endPosition)}'


class Game:
    def __init__(self, board=None):
        if board is not None:
            self.board = board
            self.gameBoard = self.board.gameboard
            return
        self.board = Board()
        self.gameBoard = self.board.gameboard
        print("Please type the location of the piece, and then the destination to play a move. Type \"Resign\" to forfeit the game")
        print("Example - \"e2 e4\"")

    def isValidMove(self, startPos, endPos, piece: Piece, isWhiteMove):
        colorOfOpponent = BLACK if isWhiteMove else WHITE
        myColour = WHITE if isWhiteMove else BLACK
        if not piece.isValid(startPos, endPos, myColour, self.board):
            return False
        boardAfterMove = Board(self.gameBoard)
        boardAfterMove.movePiece(startPos, endPos, piece)
        if boardAfterMove.isChecked(colorOfOpponent):
            return False
        return True

    def getAllValidMoves(self, color):
        allValidMoves = []
        for y in range(len(self.gameBoard)):
            for x in range(len(self.gameBoard[y])):
                piece = self.board.getPiece(x, y)
                if piece is None or piece.Color != color:
                    continue
                currentPosition = (x, y)
                movesForThisPiece = []
                for endPos in piece.availableMoves(x, y, self.board):
                    if not piece.isValid(currentPosition, endPos, piece, self.board):
                        continue
                    movesForThisPiece.append(
                        Move(currentPosition, endPos, piece))
                # movesForThisPiece = [Move(currentPosition, endPos, piece) for endPos in piece.availableMoves(
                #     *currentPosition, self.board) if self.isValidMove(currentPosition, endPos, piece, color == WHITE)]
                allValidMoves.extend(movesForThisPiece)
        return allValidMoves

    def gameStatus(self, isWhiteChance):
        myColour = WHITE if isWhiteChance else BLACK
        oppositeColor = BLACK if isWhiteChance else WHITE
        allMoves = self.getAllValidMoves(oppositeColor)
        allValidMoves = []
        for move in allMoves:
            if self.isValidMove(move.startPosition, move.endPosition, move.piece, not isWhiteChance):
                allValidMoves.append(move)

        if len(allValidMoves) > 0:
            return GAME
        print("\n")
        print(self.board)
        if self.board.isChecked(myColour):
            return CHECKMATE
        else:
            return STALEMATE
