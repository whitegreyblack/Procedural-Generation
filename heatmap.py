import random
import pprint
import color
import numpy
import math
hvalues = {
    0: 0.05,
    1: 0.2,
    2: 0.4,
    3: 0.6,
    4: 0.8,
    5: 1.0
}
def norm(x, mina, maxi): return ((x-mina)/(maxi-mina))
def val(x, y): return x*y

class HM:
    def __init__(self, size):
        def bol(x): return -((x-size)**2)+(size**2)
        def log(x): return math.log((x+1)**2)
        self.size = size
        self.heat = [[x/float(size-1) for x in range(size)] for y in range(size)]

    def vanilla(self):
        self.mini, self.maxa = 0, 0
        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                self.mini = self.heat[x][y] if self.heat[x][y] < self.mini else self.mini
                self.maxa = self.heat[x][y] if self.heat[x][y] > self.maxa else self.maxa
        return self.mini, self.maxa

    def applyFractal(self, fractal):
        wmin, wmax = 0, 0
        self.mini, self.maxa = 0, 0
        for x in range(len(fractal)):
            for y in range(len(fractal[0])):
                wmin = fractal[x][y] if fractal[x][y] < wmin else wmin
                wmax = fractal[x][y] if fractal[x][y] > wmax else wmax
        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                # this model goes from cold(top) -> hot(bottom)'
                #                        0.0->1.0               0 -> 1
                normal = norm(fractal[x][y], float(wmin), float(wmax))
                self.heat[x][y] = self.heat[x][y] * norm(fractal[x][y], float(wmin), float(wmax))
                self.mini = self.heat[x][y] if self.heat[x][y] < self.mini else self.mini
                self.maxa = self.heat[x][y] if self.heat[x][y] > self.maxa else self.maxa
        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                normal = norm(self.heat[x][y], self.mini, self.maxa)
                self.heat[x][y] = norm(self.heat[x][y], self.mini, self.maxa)

    def applyHeight(self, height):
        self.mini, self.maxa = 0, 0
        hmin, hmax = 0, 0
        for x in range(len(height)):
            for y in range(len(height[0])):
                hmin = height[x][y] if height[x][y] < hmin else hmin
                hmax = height[x][y] if height[x][y] > hmax else hmax
        for x in range(len(height)):
            for y in range(len(height[0])):
                height[x][y] = norm(height[x][y], float(hmin), float(hmax))
                
        print(hmin, hmax)
        print(self.heat[x][y], height[x][y])
        pprint.pprint(numpy.matrix(height))
        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                if 0.0 <= height[x][y] < 0.25:
                    self.heat[x][y] -= height[x][y]
                if 0.25 <= height[x][y] < 0.5:
                    self.heat[x][y] -= height[x][y] * .75
                if 0.5 <= height[x][y] < 0.75:
                    self.heat[x][y] -= height[x][y] * .5
                else:
                    self.heat[x][y] -= height[x][y] *.25
                self.mini = self.heat[x][y] if self.heat[x][y] < self.mini else self.mini
                self.maxa = self.heat[x][y] if self.heat[x][y] > self.maxa else self.maxa

        # for x in range(len(self.heat)):
        #     for y in range(len(self.heat[0])):
        #         normal = norm(self.heat[x][y], self.mini, self.maxa)
        #         self.heat[x][y] = norm(self.heat[x][y], self.mini, self.maxa)

    def applyZone(self):
        copy = numpy.copy(self.heat)
        # zone coloration for biomes
        for i in range(len(self.heat)):
            for j in range(len(self.heat[0])):
                self.heat[i][j] = norm(self.heat[i][j], self.mini, self.maxa)
                if 0 <= self.heat[i][j] < val(.4, self.maxa):
                    copy[i][j] = 5
                elif val(0.4, self.maxa) <= self.heat[i][j] < val(.6, self.maxa):
                    copy[i][j] = 4
                elif val(0.6, self.maxa) <= self.heat[i][j] < val(.75, self.maxa):
                    copy[i][j] = 3
                elif val(0.75, self.maxa) <= self.heat[i][j] < val(.85, self.maxa):
                    copy[i][j] = 2
                elif val(0.85, self.maxa) <= self.heat[i][j] < val(.95, self.maxa):
                    copy[i][j] = 1
                else:
                    copy[i][j] = 0
        return copy