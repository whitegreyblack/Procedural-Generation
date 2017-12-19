import random
import pprint
import copy
from collections import namedtuple
from PIL import Image, ImageDraw
from heightmap import steps_9_way
'''
So for every map algorithm it returns a value between 0 - 1.
This is achieved by letting each algorithm run its function and
then at the end of the process, we normalize the map to create a 
an array of floats between those two numbers.
This allows for a standarization of all map algorithms to use 
the same functions in the inherited Map class which are created
to act on an array consisiting of these float values. Any array
holding values outside of 0 to 1 will see errors in the final
product
'''

point = namedtuple("Point", ("a", "b"))

class DS:
    """ Returns a list of lists of size (2^n)+1 of values ranging from 0-255 """
    def __init__(self, size=65, maxa=255, offset=2.0, power=-0.75, n=50, seed=None):
        random.seed(seed)
        self.seed = seed if seed else random.randint(0, 99999)
        self.size = size
        self.value = maxa // 2
        self.center = size // 2
        self.offset = offset
        self.power = power
        self.world = [[0 for j in range(self.size)] for i in range(self.size)]
        self.num = 50
        self.initialize()

    def initialize(self, nw=0, sw=0, ne=0, se=0):
        """@Parameters (n: ?, a=NW, b=SW, c=NE, d=SE)"""
        # a b
        # d c
        s = self.size - 1 # set to list coordinates        
        self.set_point_safe(0, 0, nw if nw else random.randint(0, self.value))
        self.set_point_safe(0, s, sw if sw else random.randint(0, self.value))
        self.set_point_safe(s, 0, ne if ne else random.randint(0, self.value))
        self.set_point_safe(s, s, se if se else random.randint(0, self.value))

        self.diamondsquare(0, 0, s, s, self.value)

    def set_point(self, x, y, v):
        if not v:
            v = random.randint(0, self.value)
        self.world[y][x] = v

    def set_point_safe(self, x, y, v):
        if not self.world[y][x]:
            self.set_point(x, y, v)
        
    def mid(self, a, b): 
        return (a + b) // 2

    def tget(self):
        values = []
        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    values.append(self._get(i,j))
        return values
    def lget(self):
        return self.world[0]
    def rget(self):
        return self.world[self.size-1]
    def tset(self, l):
        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    self.world[i][j] = l[i]
    def lset(self, l):
        self.world[0] = l
    def rset(self, l):
        self.world[self.size-1] = l
    def _add(self, l, x, y):
        l.extend([self._get(x,y)]*self.num)
        return l

    def _tot(self, x):
        return sum(x)/len(x)

    def _mul(self, a, b=1): 
        return self._int((random.random() - 0.5) * a * b)

    def _int(self, x): 
        return int(round(x))

    def _smooth(self, x, y):
        neighbors = []
        for i in range(-1, 1):
            for j in range(-1, 1):
                if (x, y) != (x+i, y+j):
                    try:
                        neighbors.append(self._get(x+i, y+j))
                    except:
                        pass
        return self._tot([self._tot(neighbors), self._get(x, y)])
        #return self._tot(neighbors)
    def smooth(self):
        for i in range(1, self.size):
            for j in range(1, self.size):
                self._set(i, j, self._smooth(i, j))

    def minmax(self):
        self.min, self.max = 0, 0
        for i in range(self.size):
            for j in range(self.size):
                self.min = self._get(i,j) if self._get(i,j) < self.min else self.min
                self.max = self._get(i,j) if self._get(i,j) > self.max else self.max

    def neighbors(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_9_way()]

    def smooth(self):
        world = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                num = 0
                value = 0
                for xx, yy in self.neighbors(x, y):
                    try:
                        value += self.world[yy][xx]
                        num += 1
                    except IndexError:
                        pass
                world[y][x] = value//num
        self.world = world

    def normalize(self):
        world = copy.deepcopy(self.world)
        for y in range(self.size):
            for x in range(self.size):
                world[y][x] = self._normalize(self.world[y][x])
        self.world = world

    def _sum(self, x, y, l ,t, r, b, v):
        if not v:
            return self._tot([self._get(l, t), self._get(r, t), self._get(l, b), self._get(r, b)])
        else:
            tm = [self._get(l, t), self._get(r, t)]
            bm = [self._get(l, b), self._get(r, b)]
            lm = [self._get(l, t), self._get(l, b)]
            rm = [self._get(r, t), self._get(r, b)]
        
            return (self._tot(self._add(tm, x, y)),
                self._tot(self._add(bm, x, y)),
                self._tot(self._add(lm, x, y)),
                self._tot(self._add(rm, x, y)))

    def diamondsquare(self, l, t, r, b, d):
        x = self.mid(l, r)
        y = self.mid(t, b)

        cm = self._sum(x, y, l, t, r, b, 0)
        self.sset(x, y, self._int(cm - self._mul(d, 2))) 

        tm, bm, lm, rm = self._sum(x, y, l, t, r, b, 1)
        self.sset(x, t, self._int(tm + self._mul(d)))
        self.sset(x, b, self._int(bm + self._mul(d)))
        self.sset(l, y, self._int(lm + self._mul(d)))
        self.sset(r, y, self._int(rm + self._mul(d)))

        if (r - l) > 2:
            d = self._int(d * self.offset ** self.power)
            self.diamondsquare(l, t, x, y, d)
            self.diamondsquare(x, t, r, y, d)
            self.diamondsquare(l, y, x, b, d)
            self.diamondsquare(x, y, r, b, d)

    def integer_to_hex(self, value):
        value = hex(value).split('x')[1]
        if len(value) < 2:
            value = "0" + value
        return '#' + value * 3

    def _normalize(self, value):
        return int((value - self.min) / (self.max - self.min) * 250)

    def output_image(self, colored=False):
        self.smooth()
        self.normalize()
        self.minmax()
        
        img = Image.new('RGB', (self.size * 8, self.size * 8))
        ids = ImageDraw.Draw(img)

        if colored:
            for y in range(self.size):
                for x in range(self.size):
                    value = self.integer_to_hex(self._normalize(self.world[y][x]))
                    ids.rectangle([x * 8, y * 8, x * 8 + 8, y * 8 + 8], value)
        else:
            for y in range(self.size):
                for x in range(self.size):
                    if world[y][x] > 200:
                        ids.rectangle(
                            [x * 8, y * 8, x * 8 + 8, y * 8 + 8], 
                            '#ffffff')
                    elif 150 < world[y][x] < 200:
                        ids.rectangle(
                            [x * 8, y * 8, x * 8 + 8, y * 8 + 8], 
                            '#808080')
                    elif 100 < world[y][x] < 150:
                        ids.rectangle(
                            [x * 8, y * 8, x * 8 + 8, y * 8 + 8], 
                            '#00FF00')
                    else:
                        ids.rectangle(
                            [x * 8, y * 8, x * 8 + 8, y * 8 + 8], 
                            '#0000ff')                   
        img.save('diamondsquareflat.png')

if __name__ == "__main__":
    dsf = DS(size=124, n=50)
    dsf.output_image(True)