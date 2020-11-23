from .Game import Game, CHECKMATE, Move, STALEMATE, GAME
from .Board import *
from .Pieces import WHITE, BLACK
from .helperFunctions import *


class Engine:
    DEPTH = 3

    def getBestMove(self, board: Board, isWhiteMove):
        g = Game(board)
        bestMoveEval = -10000 if isWhiteMove else 10000
        bestMoveFound = None
        for move in g.getAllValidMoves(WHITE if isWhiteMove else BLACK):
            boardAfterMove = Board(board.gameboard)
            boardAfterMove.movePiece(
                move.startPosition, move.endPosition, move.piece)
            value = - self.minimax(boardAfterMove, self.DEPTH -
                                   1, -10001, 10001, not isWhiteMove)
            if (isWhiteMove and value >= bestMoveEval) or (not isWhiteMove and value <= bestMoveEval):
                bestMoveEval = value
                bestMoveFound = move
        return bestMoveFound

    def selectmove(self, board: Board, isWhiteMove):
        bestMove = None
        bestValue = -9999
        alpha = -10000
        beta = 10000
        g = Game(board)
        for move in g.getAllValidMoves(WHITE if isWhiteMove else BLACK):
            boardAfterMove = Board(board.gameboard)
            boardAfterMove.movePiece(
                move.startPosition, move.endPosition, move.piece)
            boardValue = -self.alphabeta(boardAfterMove, -beta, -alpha,
                                         self.DEPTH-1, not isWhiteMove)
            if boardValue > bestValue:
                bestValue = boardValue
                bestMove = move
            if(boardValue > alpha):
                alpha = boardValue
        return bestMove

    def alphabeta(self, board: Board, alpha, beta, depthleft, isWhiteMove: bool):
        bestscore = -10000
        if(depthleft == 0):
            return self.evaluation(board, isWhiteMove)
        game = Game(board)
        for move in game.getAllValidMoves(WHITE if isWhiteMove else BLACK):
            boardAfterMove = Board(board.gameboard)
            boardAfterMove.movePiece(
                move.startPosition, move.endPosition, move.piece)
            score = - self.alphabeta(boardAfterMove, -
                                     beta, -alpha, depthleft - 1, not isWhiteMove)
            if(score >= beta):
                return score
            if(score > bestscore):
                bestscore = score
            if(score > alpha):
                alpha = score
        return bestscore

    def minimax(self, board: Board, depth: int, alpha: int, beta: int, maximizingPlayer: bool):
        if depth == 0:
            return - self.evaluation(board, maximizingPlayer)
        g = Game(board)
        # gameStatus = g.gameStatus(not maximizingPlayer)
        # if gameStatus == CHECKMATE:
        #     return (-10000 if maximizingPlayer else 10000), None
        # if gameStatus == STALEMATE:
        #     return 0, None

        if maximizingPlayer:
            maxEval = -10000
            for move in g.getAllValidMoves(WHITE):
                boardAfterMove = Board(board.gameboard)
                boardAfterMove.movePiece(
                    move.startPosition, move.endPosition, move.piece)
                maxEval = max(maxEval, self.minimax(
                    boardAfterMove, depth-1, alpha, beta, not maximizingPlayer))
                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    break
            return maxEval

        else:
            minEval = 10000
            for move in g.getAllValidMoves(BLACK):
                boardAfterMove = Board(board.gameboard)
                boardAfterMove.movePiece(
                    move.startPosition, move.endPosition, move.piece)
                minEval = min(minEval, self.minimax(
                    boardAfterMove, depth-1, alpha, beta, not maximizingPlayer))
                beta = min(beta, minEval)
                if beta <= alpha:
                    break
            return minEval

    def evaluation(self, board: Board, isWhiteChance: bool):
        g = Game(board)
        gameStatus = g.gameStatus(isWhiteChance)
        if gameStatus == STALEMATE:
            return 0
        if gameStatus == CHECKMATE:
            return 10000 if isWhiteChance else -10000
        evaluationScore = 0
        for y in range(8):
            for x in range(8):
                piece = board.getPiece(x, y)
                if piece is None:
                    continue
                evaluationScore += getPieceValue(piece)
                evaluationScore += piece.posEval(x, y)

        return evaluationScore
