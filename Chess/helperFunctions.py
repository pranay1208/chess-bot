def parsePositon(position):
    x = ord(position[0]) - ord('a')
    y = int(position[1]) - 1
    return x, y


def coordToPosition(coord):
    (x, y) = coord
    return f'{chr(x+ord("a"))}{y+1}'
