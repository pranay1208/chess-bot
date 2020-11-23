from .Pieces import *


def parsePositon(position):
    x = ord(position[0]) - ord('a')
    y = int(position[1]) - 1
    return x, y


def coordToPosition(coord):
    (x, y) = coord
    return f'{chr(x+ord("a"))}{y+1}'


def getPieceValue(piece: Piece):
    valueDict = {
        "♖": 50,
        "♜": -50,
        "♘": 30,
        "♞": -30,
        "♗": 30,
        "♝": -30,
        "♕": 90,
        "♛": -90,
        "♔": 1000,
        "♚": -1000,
        "♙": 10,
        "♟": -10
    }
    return valueDict[str(piece)]
