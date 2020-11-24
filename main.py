from Chess.Board import Board
from Chess.Pieces import *
from Chess.helperFunctions import *
from Chess.Game import *
from Chess.Engine import *
import time


def main():
    game = Game()
    startGame(game)
    # moves = []
    # for m in moves:
    #     start, end = m.split()
    #     start = parsePositon(start)
    #     end = parsePositon(end)
    #     piece = game.board.getPiece(*start)
    #     game.board.movePiece(start, end, piece)
    # print(game.board)
    # for a in game.getAllValidMoves(BLACK):
    #     print(a)


def startGame(game: Game):
    playerMoveWhite = True
    while(True):
        if playerMoveWhite:
            print(game.board)
        if not playerMoveWhite:
            engine = Engine()
            startTime = time.time()
            move = engine.selectmove(game.board, False)
            if move is None:
                print("Black resigns")
                break
            game.board.movePiece(move.startPosition,
                                 move.endPosition, move.piece)
            print("Black moves", move, "taking",
                  time.time()-startTime, "seconds")
        else:
            userMove = input()
            if userMove == "Resign" or userMove == "resign":
                break
            try:
                start, end = userMove.split()
                start = parsePositon(start)
                end = parsePositon(end)
                piece = game.board.getPiece(*start)
            except:
                print("Invalid command")
                continue
            if piece is None:
                print("No piece exists there")
                continue
            if piece.Color != WHITE:
                print("That piece is not yours")
                continue
            if not game.isValidMove(start, end, piece, True):
                print("Invalid move")
                continue
            game.board.movePiece(start, end, piece)

        gs = game.gameStatus(playerMoveWhite)
        if gs == GAME:
            playerMoveWhite = not playerMoveWhite
            print()
        elif gs == CHECKMATE:
            print("CHECKMATE", "WHITE" if playerMoveWhite else "BLACK", "wins")
            break
        else:
            print("STALEMATE game draw")
            break
    # e, a = Engine().minimax(Board(), 4, -math.inf, math.inf, False)
    # print(e, a)


if __name__ == "__main__":
    main()
    pass
