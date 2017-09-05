import random


class DS:
    """ Returns a list of lists of size (2^n)+1 of values ranging from 0-255 """

    def __init__(self, size=64, maxa=255, seed=random.randint(
            0, 9999), offset=2.0, power=-0.75):
        random.seed(seed)
        self.seed = seed
        self.size = size
        self.value = maxa / 2
        self.center = size / 2
        self.offset = offset
        self.power = power

    def initialize(self, n, a=None, b=None, c=None, d=None):
        # a b
        # d c
        def setpoint(x, y, v=None):
            self.map[x][y] = self.value if not v else v
        self.num = n
        self.map = [[0 for j in range(self.size)] for i in range(self.size)]
        s = self.size - 1  # set to list coordinates
        setpoint(0, 0, a)
        setpoint(0, s, b)
        setpoint(s, 0, d)
        setpoint(s, s, c)
        self.diamondsquare(0, 0, s, s, self.value)

    def _mid(self, a, b):
        return (a + b) / 2

    def _get(self, a, b):
        return self.map[a][b]

    def _set(self, a, b, c):
        self.map[a][b] = c

    def sset(self, a, b, c):
        self.map[a][b] = c if self._get(a, b) is 0 else self._get(a, b)

    def _add(self, l, x, y):
        l.extend([self._get(x, y)] * self.num)
        return l

    def _tot(self, x):
        return sum(x) / len(x)

    def _mul(self, a, b=1):
        return self._int((random.random() - 0.5) * a * b)

    def _int(self, x):
        return int(round(x))

    def _smooth(self, x, y):
        neighbors = []
        for i in range(-1, 1):
            for j in range(-1, 1):
                if (x, y) != (x + i, y + j):
                    try:
                        neighbors.append(self._get(x + i, y + j))
                    except BaseException:
                        pass
        return self._tot([self._tot(neighbors), self._get(x, y)])

    def smooth(self):
        for i in range(self.size):
            for j in range(self.size):
                self._set(i, j, self._smooth(i, j))

    def _sum(self, x, y, l, t, r, b, v):
        if not v:
            return self._tot([self._get(l, t), self._get(
                r, t), self._get(l, b), self._get(r, b)])
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


class


class HeatMap:
    def __init__(self, map)
