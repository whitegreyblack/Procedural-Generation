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
        self.world = [[(random.random()*2-1) for j in range(height)] for i in range(width)]
        self.maxa = 0.0
        self.mini = 0.0
        self.subdivide((0,0), (width-1, height-1), delta)
        #print(self.world)
        self.smooth()

    def subdivide(self, a, b, delta):
        def point(a=None, b=None, c=None, d=None):
            total = 0.0
            point = 0.0
            if a:
                ax, ay = a
                total += self.world[ax][ay]
                point += 1
            if b:
                bx, by = b
                total += self.world[bx][by]
                point += 1
            if c:
                cx, cy = c
                total += self.world[cx][cy]
                point += 1
            if d:
                dx, dy = d
                total += self.world[dx][dy]
                point += 1
            return total/point
        
        def points(l=[]):
            total, point = 0.0, 0
            for i in l:
                ix, iy = i
                total += self.world[ix][iy]
                point += 1
            return total/point

        def setter(x):
            if x < self.mini:
                self.mini = x
            if x > self.maxa:
                self.maxa = x
            return x

        x1, y1 = a
        x9, y9 = b
        x7, y7 = x1, y9
        x3, y3 = x9, y1
        if x1+1 >= x9 and y1+1 >= y9:
            return

        dz = (random.random()*2-1)*delta

        # diamond
        x5, y5 = (x1+x9)/2, (y1+y9)/2
        self.world[x5][y5] = setter(point((x1,y1),(x3,y3),(x7,y7),(x9,y9)) + dz)

        # square
        x2, y2 = (x1+x3)/2, (y1+y3)/2
        self.world[x2][y2] = setter(point((x1,y1),(x3,y3))+dz)

        x4, y4 = (x1+x7)/2, (y1+y7)/2
        self.world[x4][y4] = setter(point((x1,y1),(x7,y7))+dz)

        x6, y6 = (x3+x9)/2, (y3+y9)/2
        self.world[x6][y6] = setter(point((x3,y3),(x9,y9))+dz)

        x8, y8 = (x7+x9)/2, (y7+y9)/2
        self.world[x8][y8] = setter(point((x7,y7),(x9,y9))+dz)

        delta *= self.noise
        self.subdivide((x1,y1), (x5,y5), delta)
        self.subdivide((x2,y2), (x6,y6), delta)
        self.subdivide((x4,y4), (x8,y8), delta)
        self.subdivide((x5,y5), (x9,y9), delta)

    def normalize(self):
        for x in range(len(self.world)):
            for y in range(len(self.world[x])):
                self.world[x][y] = int(round(((self.world[x][y]-self.mini)/(self.maxa-self.mini))*250))

    def smooth(self):
        def point(x, y):
            total = 0
            w = len(self.world)
            h = len(self.world[0])
            total += self.world[(x-1)%w][(y-1)%h]
            total += self.world[(x+0)%w][(y-1)%h]
            total += self.world[(x+1)%w][(y-1)%h]
            total += self.world[(x-1)%w][(y-0)%h]
            total += self.world[(x+0)%w][(y-0)%h]
            total += self.world[(x+1)%w][(y-0)%h]
            total += self.world[(x-1)%w][(y+1)%h]
            total += self.world[(x+0)%w][(y+1)%h]
            total += self.world[(x+1)%w][(y+1)%h]
            total /= 9
            return total
        for x in range(len(self.world)):
            for y in range(len(self.world[x])):
                self.world[x][y] = int(round(((point(x, y)-self.mini)/(self.maxa-self.mini))*250))


    def heightlist(self):
        def bucket(i):
            buckets = [(250/x)*(x-1) for x in range(i)]
        height = dict()
        for x in range(len(self.world)):
            for y in range(len(self.world[x])):
                val = int(round(((self.world[x][y]-self.mini)/(self.maxa-self.mini))*250))
                self.world[x][y] = val
                if val in height:
                    height[val] += 1
                else:
                    height[val] = 1
        sorted(height, reverse=True)
        print(height)
        print(len(height.keys()))
pvar = "{}: {}"

''' initialize '''
WIDTH, HEIGHT = 300, 150
tdl.setFont('4x6.png')
console = tdl.init(WIDTH, HEIGHT, 'heightmap')
plane = MPD(WIDTH, HEIGHT, .8, 1)
total = plane.maxa-plane.mini
print(plane.maxa, plane.mini, plane.maxa-plane.mini)
def level(x):
    return (250/x)*(x-1)
print(level(1))

while True:
    console.clear()
    mts = set()
    for i in range(WIDTH):
        for j in range(HEIGHT):
            val = plane.world[i][j]
            # console.draw_char(i, j, '#', (val, val, val))
            if 250 == val:
                console.draw_char(i, j, '^', color.WHITE)
                mts.add(val)
            elif level(25) <= val < 250: 
                console.draw_char(i, j, '^', color.LGRAY)
            elif level(24) <= val < level(25):
                console.draw_char(i, j, 'n', color.MGRAY)
            elif level(23) <= val < level(24):
                console.draw_char(i, j, 'n', color.HGRAY)
            elif level(22) <= val < level(23):
                console.draw_char(i, j, 'n', color.DGRAY)
            elif level(20) <= val < level(22):
                console.draw_char(i, j, '*', color.DGREEN)
            elif level(5) <= val < level(20):
                console.draw_char(i, j, '*', (0,val,val//2))
            else:
                console.draw_char(i, j, 'o', (0, val//2, val))
    tdl.flush()
    for event in tdl.event.get():
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
            raise SystemExit('The window has been closed.')
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 's'):
            plane.smooth()
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'd'):
            plane.subdivide((0,0), (WIDTH-1, HEIGHT-1), 50)
        if event.type == 'QUIT':
            raise SystemExit('The window has been closed.')