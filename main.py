from Chess.Board import Board
from Chess.Pieces import *
from Chess.helperFunctions import *
from Chess.Game import Game
import math


def minimax(position: Board, depth: int, alpha: int, beta: int, maximisingPlayer: bool):
    if depth == 0 or position.isGameOver():
        return position.eval()

    if maximisingPlayer:
        maxEval = -math.inf
        for child in position.children():
            eval = minimax(child, depth-1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = math.inf
        for child in position.children():
            eval = minimax(child, depth-1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta - min(beta, minEval)
            if beta <= alpha:
                break
        return minEval


def main1():
    b = Board()
    # minimax(b, 3, -math.inf, math.inf, True)  # for white
    color = WHITE
    while(True):
        print()
        print(b)
        i = input()
        if(i == "exit"):
            break
        f, to = i.split()
        f = parsePositon(f)
        to = parsePositon(to)
        piece = b.getPiece(*f)
        if piece is None:
            print("No piece there")
            continue
        if piece.Color != color:
            print("Not your turn")
            continue
        if piece.isValid(f, to, color, b):
            b.movePiece(f, to, piece)
            if b.isChecked(color):
                print(color, "checks")
            if color == BLACK:
                color = WHITE
            else:
                color = BLACK
        else:
            print("Invalid move")


def main():
    game = Game()
    game.startGame()


if __name__ == "__main__":
    main()
    pass
