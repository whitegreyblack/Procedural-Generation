import random
import numpy
import pprint

class DS:
    """ Returns a list of lists of size (2^n)+1 of values ranging from 0-255 """
    def __init__(self, size=65, maxa=255, seed=random.randint(0,9999), offset=2.0, power=-0.75):
        random.seed(seed)
        self.seed = seed
        self.size = size
        self.value = maxa/2
        self.center = size / 2
        self.offset = offset
        self.power = power
        self.map = [[0 for j in range(self.size)] for i in range(self.size)]

    def initialize(self, n, a=None, b=None, c=None, d=None):
        # a b
        # d c
        def setpoint(x, y, v=None): 
            self.sset(x, y, random.randint(0, self.value*2)) if not v else self.sset(x, y, v)
        self.num = n
        s = self.size-1 # set to list coordinates        
        setpoint(0, 0, a)
        setpoint(0, s, b)
        setpoint(s, 0, d)
        setpoint(s, s, c)
        self.diamondsquare(0, 0, s, s, self.value)
        
    def _mid(self, a, b): 
        return (a+b)/2

    def _get(self, a, b): 
        return self.map[a][b]

    def _set(self, a, b, c): 
        self.map[a][b] = c

    def sset(self, a, b, c): 
        self.map[a][b] = c if self._get(a,b) is 0 else self._get(a, b)
    def tget(self):
        values = []
        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    values.append(self._get(i,j))
        return values
    def lget(self):
        return self.map[0]
    def rget(self):
        return self.map[self.size-1]
    def tset(self, l):
        for i in range(self.size):
            for j in range(self.size):
                if j == 0:
                    self.map[i][j] = l[i]
    def lset(self, l):
        self.map[0] = l
    def rset(self, l):
        self.map[self.size-1] = l
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

    def normalize(self, val):
        self.minmax()
        def norm(x):
                # print('x', x, x-self.min, float(self.max-self.min), (x-self.min)/float(self.max-self.min))
                return self._int((x-self.min)/float(self.max-self.min)*val)

        copy = numpy.copy(self.map)
        for i in range(self.size):
            for j in range(self.size):
                copy[i][j] = norm(float(self._get(i, j)))
        return copy

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
        x = self._mid(l, r)
        y = self._mid(t, b)

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

  