import tdl
import math
import copy
import graph
import color
import random
import movement
from bearlibterminal import terminal
class MPD:
    def __init__(self, size, height):
        self.world = [height//2 for i in range(size)]

    def subdivide(self, x, y, z):
        if y-x <= 1:
            return
        self.world[x] = random.randint(0, 50-z)
        self.world[y] = random.randint(0, 50-z)
        self.subdivide(x, (x+y)//2, z+1)
        self.subdivide((x+y)//2, y, z+1)

    def serialdivide(self, x, y, z=None):
        if z == None:
            z = len(self.world)//2
        #print(x, y, z)
        if (y-x) <= 1 or x == y or z == 0:
            return
        #print(x, y, z)
        if x % len(self.world) == 0:
            self.world[x] = random.randint(0, 250)
        if y % len(self.world) == 0:
            self.world[y] = random.randint(0, 250)
        self.world[x] = self.world[x-1]+random.randint(-5, 5)
        self.world[y] = self.world[(y+1)%len(self.world)]+random.randint(-5, 5)
        self.serialdivide(x+1, y-1, z-1)

    def smooth(self, size):
        #print('smoothing')
        for x in range(size):
            self.world[x] = (self.world[x-1]+self.world[x]+self.world[(x+1)%(size)])//3

class MPD2D:
    def __init__(self, x, y):
        self.world = [[graph.Tile(i, j) for j in range(y)] for i in range(x)]
        self.populate((0,0), (x-1,y-1))
        random.seed(random.randint(0, 9999))

    def populate(self, a, b):
        x0, y0 = a
        x1, y1 = b
        self.world[x0][y0].height = random.randint(25, 200) # q4
        self.world[x0][y0].foreground = (0, 0, 250)
        self.world[x1][y0].height = random.randint(25, 200) # q1
        self.world[x1][y0].foreground = (0, 250, 0)
        self.world[x0][y1].height = random.randint(25, 200) # q3
        self.world[x0][y1].foreground = (250, 0, 0)
        self.world[x1][y1].height = random.randint(25, 200) # q2
        self.world[x1][y1].foreground = (250, 250, 50)
        
        # subdivide
        for i in range(1):
            self.divide(a, b, .8) 

        self.maxa('t')

    def divide(self, a, c, roughness):
        ax, ay = a
        cx, cy = c

        bx, by = cx, ay
        dx, dy = ax, cy
        
        # DIAMOND COORDINATES
        x5, y5 = (ax+bx+cx+dx)//4, (ay+by+cy+dy)//4
        self.world[x5][y5] += self.world[ax][ay]
        self.world[x5][y5] += self.world[bx][by]
        self.world[x5][y5] += self.world[cx][cy]
        self.world[x5][y5] += self.world[dx][dy]

        # print(self.world[x5][x5])

        # SQUARE COORDINATES
        x1, y1 = (ax+bx)//2, (ay+by)//2
        self.world[x1][y1] += self.world[ax][ay]
        self.world[x1][y1] += self.world[bx][by]

        x2, y2 = (bx+cx)//2, (by+cy)//2
        self.world[x2][y2] += self.world[bx][by]
        self.world[x2][y2] += self.world[by][cy]

        x3, y3 = (cx+dx)//2, (cy+dy)//2
        self.world[x3][y3] += self.world[cx][cy]
        self.world[x3][y3] += self.world[dx][dy]

        x4, y4 = (ax+dx)//2, (ay+dy)//2
        self.world[x4][y4] += self.world[ax][ay]
        self.world[x4][y4] += self.world[dx][dy]

        # subdivide each square
        if (ay+(cy-ay)//2) > ay:
             self.divide((x1, y1), (x5, y5), roughness*3//4)
             self.divide((x1, y1), (x2, y2), roughness*3//4)
             self.divide((x5, y5), (cx-1, cy-1), roughness*3//4)
             self.divide((x4, y4), (x3, y3), roughness*3//4)

    def neighbor(self, x, y):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (x, y):
                    total += self.world[(x+i)%len(self.world)][(y+j)%len(self.world[0])].height
        return total

    def smooth(self):
        self.maxa()
        newmaxa = 0
        newworld = copy.deepcopy(self.world)
        height = set()
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                newworld[i][j].height = self.neighbor(i, j)//self.height
                if newworld[i][j].height > newmaxa:
                    newmaxa = newworld[i][j].height
        self.world = newworld
        self.height = newmaxa

    def maxa(self, a=None):
        height = set()
        high = 0
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                height.add(self.world[i][j].height)
                if self.world[i][j].height > high:
                    high = self.world[i][j].height
        self.height = high
        #if a:
            #print(height)
# pvar = "{}: {}"

# ''' initialize '''
# WIDTH, HEIGHT = 60, 180

# plane = MPD2D(WIDTH, HEIGHT)
# #print(plane.height)
# lines = []
# for i in range(WIDTH):
#     line = ""
#     for j in range(HEIGHT):
#         val = plane.world[i][j].height * 255 / plane.height
#         line += "#" if val > 0 else " "
# #            val = plane.world[i][j].height * 255 / plane.height
#     lines.append(line)
# print("\n".join(lines))

if __name__ == "__main__":
    width, height = 80, 25
