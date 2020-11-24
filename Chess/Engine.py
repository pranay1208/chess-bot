from .Game import Game, CHECKMATE, Move, STALEMATE, GAME
from .Board import *
from .Pieces import WHITE, BLACK
from .helperFunctions import *


class Engine:
    DEPTH = 3

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
                evaluationScore += piece.posEval(x, y)/10
                if piece.max_possible_moves != 0:
                    numFreeMoves = len(piece.availableMoves(x,  y, board))
                    if numFreeMoves == 0:
                        # if piece cannot move, it's value is halved
                        evaluationScore -= getPieceValue(piece)/2
                    else:
                        numFreeMovesMultiplier = 1 if piece.Color == WHITE else -1
                        pieceUtility = numFreeMoves / piece.max_possible_moves
                        evaluationScore += (numFreeMovesMultiplier *
                                            pieceUtility / 25)

        return evaluationScore
