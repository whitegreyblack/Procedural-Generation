import math
import copy
import graph
import color
import graph
import random
import movement

class MPD:
    def __init__(self, width, height, noise, delta):
        self.noise = noise
        self.width = width
        self.height = height
        self.world = [[(random.random()*2-1) for j in range(height)] for i in range(width)]
        self.maxa = 0.0
        self.mini = 0.0
        self.diamondsquare((0,0), (width-1, height-1), delta)

    def diamondsquare(self, a, b, delta):
        x1, y1 = a
        x9, y9 = b
        x7, y7 = x1, y9
        x3, y3 = x9, y1
        dz = (random.random()*2-1*1)*delta
        x, y = (x9+x1)//2, (y9+y1)//2
        if x < 1 or y < 1: 
            return
        
        self.diamondsquare((0,0), ((x9+x1)//2,(y9+y1)//2), delta)

''' initialize '''
WIDTH, HEIGHT = 128, 128
plane = MPD(WIDTH, HEIGHT, .8, 50)


def level(x):
    return (250/x)*(x-1)

mts = set()
lines = []
for i in range(WIDTH):
    line = ""
    for j in range(HEIGHT):
        line += "." if line else " "
    lines.append(line)
print("\n".join(lines))
