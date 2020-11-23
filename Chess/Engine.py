import math
from .Game import Game, CHECKMATE, STALEMATE, GAME
from .Board import *
from .Pieces import WHITE, BLACK
from .helperFunctions import *


class Engine:

    def getBestMove(self, board, isWhiteMove):
        return self.minimax(board, 2, -math.inf, math.inf, isWhiteMove)[1]
    # def __init__(self):

    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
        if depth == 0:
            return self.evaluation(board), None
        g = Game(board)
        gameStatus = g.gameStatus(not maximizingPlayer)
        if gameStatus == CHECKMATE:
            return (-math.inf if maximizingPlayer else math.inf), None
        if gameStatus == STALEMATE:
            return 0, None

        if maximizingPlayer:
            maxEval = -math.inf
            bestMove = None
            for move in g.getAllValidMoves(WHITE):
                boardAfterMove = Board(board.gameboard)
                boardAfterMove.movePiece(
                    move.startPosition, move.endPosition, move.piece)
                eVal, nextMoves = self.minimax(
                    boardAfterMove, depth - 1, alpha, beta, False)
                if maxEval < eVal:
                    maxEval = eVal
                    bestMove = move

                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval, bestMove

        else:
            minEval = math.inf
            bestMove = None
            for move in g.getAllValidMoves(BLACK):
                boardAfterMove = Board(board.gameboard)
                boardAfterMove.movePiece(
                    move.startPosition, move.endPosition, move.piece)
                eVal, nextMoves = self.minimax(
                    boardAfterMove, depth-1, alpha, beta, True)
                if minEval > eVal:
                    minEval = eVal
                    bestMove = move

                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval, bestMove

    def evaluation(self, board: Board):
        evaluationScore = 0
        for y in range(len(board.gameboard)):
            for x in range(len(board.gameboard[y])):
                piece = board.getPiece(x, y)
                if piece is None:
                    continue
                evaluationScore += getPieceValue(piece)

        return evaluationScore
