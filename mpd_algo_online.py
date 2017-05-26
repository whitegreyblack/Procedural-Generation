import tdl
import math
import copy
import graph
import color
import graph
import random
import logging
import movement

logging.basicConfig(level=logging.DEBUG, filename='points.log', format='%(message)s')

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
        x, y = (x9+x1)/2, (y9+y1)/2
        if x < 1 or y < 1: 
            return
        
        # diamond
        self.world[x][y]

        self.diamondsquare((0,0), ((x9+x1)/2,(y9+y1)/2), delta)

''' initialize '''
WIDTH, HEIGHT = 128, 128
tdl.setFont('4x6.png')
console = tdl.init(WIDTH, HEIGHT, 'heightmap')
plane = MPD(WIDTH, HEIGHT, .8, 50)


def level(x):
    return (250/x)*(x-1)

while True:
    console.clear()
    mts = set()
    for i in range(WIDTH):
        for j in range(HEIGHT):
            val = plane.world[i][j]
            pass
    tdl.flush()
    for event in tdl.event.get():
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
            raise SystemExit('The window has been closed.')
        if event.type == 'QUIT':
            raise SystemExit('The window has been closed.')