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
    def __init__(self, width, height, noise):
        self.noise = noise
        self.world = [random.random()*2-1 for i in range(width)]
        self.maxa = 0.0
        self.mini = 0.0

    def subdivide(self, x1, x2, delta):
        if x1+1 == x2:
            return
        x3 = (x1+x2)/2
        dy = (random.random()*2-1)*delta

        # midpoint
        self.world[x3] = (self.world[x1]+self.world[x2])/2+dy
        if self.world[x3] < self.mini:
            self.mini = self.world[x3]
        if self.world[x3] > self.maxa:
            self.maxa = self.world[x3]
        self.subdivide(x1, x3, delta*self.noise)
        self.subdivide(x3, x2, delta*self.noise)

    def serialdivide(self, x, end, delta):
        if x+2 == end:
            return
        dy = (random.random()*2-1)*delta
        self.world[x+1] = (self.world[x]+self.world[x+2])/2+dy
        if self.world[x+1] < self.mini:
            self.mini = self.world[x+1]
        if self.world[x+1] > self.maxa:
            self.maxa = self.world[x+1]
        self.subdivide(x+1, end, delta*self.noise)
        
    def smooth(self, x1=None, x2=None):
        for x in range(x1 if x1 else 0, x2 if x2 else len(self.world)):
            self.world[x] = (self.world[(x-1)%(len(self.world))]+self.world[x]+self.world[(x+1)%(len(self.world))])/3.0

pvar = "{}: {}"

''' initialize '''
WIDTH, HEIGHT = 300, 60
tdl.setFont('4x6.png')
console = tdl.init(WIDTH, HEIGHT, 'heightmap')

line = MPD(WIDTH, HEIGHT, .7)
line.subdivide(0, WIDTH-1, 50)
#line.serialdivide(0, WIDTH-1, 50)
total = line.maxa-line.mini
while True:
    console.clear()
    for i in range(WIDTH):
        console.draw_char(i, int(round((line.world[i]-line.mini)/(total)*HEIGHT)), 'o')
        # console.draw_char(i, int(round(line.world[i] * HEIGHT/total + HEIGHT/total)), 'o')
    tdl.flush()
    for event in tdl.event.get():
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
            raise SystemExit('The window has been closed.')
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 's'):
            line.smooth()
        if event.type == 'QUIT':
            raise SystemExit('The window has been closed.')