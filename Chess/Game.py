from Chess.helperFunctions import parsePositon
from .Board import Board
from .Pieces import *
from .helperFunctions import *


class Move:
    def __init__(self, start, end, piece):
        self.startPosition = start
        self.endPosition = end
        self.piece = piece


class Game:
    def __init__(self):
        self.board = Board()
        self.gameBoard = self.board.gameboard
        print("Please type the location of the piece, and then the destination to play a move. Type \"Resign\" to forfeit the game")
        print("Example - \"e2 e4\"")

    def startGame(self):
        playerMoveWhite = True
        while(True):
            print(self.board)
            if not playerMoveWhite:
                # TODO: AI moves
                print("Black moves")
            else:
                userMove = input()
                if userMove == "Resign":
                    break
                start, end = userMove.split()
                start = parsePositon(start)
                end = parsePositon(end)
                piece = self.board.getPiece(*start)
                if piece is None:
                    print("No piece exists there")
                    continue
                if piece.Color != WHITE:
                    print("That piece is not yours")
                    continue
                if not self.isValidMove(start, end, piece, True):
                    print("Invalid move")
                    continue
                self.board.movePiece(start, end, piece)

            if self.isGameOver(playerMoveWhite):
                break
            playerMoveWhite = not playerMoveWhite
            print()

    def isValidMove(self, startPos, endPos, piece: Piece, isWhiteMove):
        colorOfOpponent = BLACK if isWhiteMove else WHITE
        if not piece.isValid(startPos, endPos, WHITE, self.board):
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
                movesForThisPiece = [Move(currentPosition, endPos, piece) for endPos in piece.availableMoves(
                    *currentPosition, self.board) if self.isValidMove(currentPosition, endPos, piece, color == WHITE)]
                allValidMoves.extend(movesForThisPiece)
        return allValidMoves

    def isGameOver(self, isWhiteChance):
        myColour = WHITE if isWhiteChance else BLACK
        oppositeColor = BLACK if isWhiteChance else WHITE
        allValidMoves = self.getAllValidMoves(oppositeColor)
        if len(allValidMoves) > 0:
            return False
        print("\n")
        print(self.board)
        if self.board.isChecked(myColour):
            print("CHECKMATE", myColour, "wins")
        else:
            print("STALEMATE: DRAW")
        print("\n")
        return True
