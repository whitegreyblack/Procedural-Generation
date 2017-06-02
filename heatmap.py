import random
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

class HM:
    def __init__(self, size):
        def bol(x): return -((x-size)**2)+(size**2)
        def log(x): return math.log((x+1)**2)
        self.size = size
        self.heat = [[bol(x)/float(bol(size)) for x in range(size)] for y in range(size)]

    def vanilla(self):
        mini, maxa = 0, 0
        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                mini = self.heat[x][y] if self.heat[x][y] < mini else mini
                maxa = self.heat[x][y] if self.heat[x][y] > maxa else maxa
        return mini, maxa

    def applyFractal(self, fractal):
        def norm(x, mina, maxi):
            return ((x-mina)/(maxi-mina))
        def val(x, y): return x*y
        wmin, wmax = 0, 0
        mini, maxa = 0, 0
        for x in range(len(fractal)):
            for y in range(len(fractal[0])):
                wmin = fractal[x][y] if fractal[x][y] < wmin else wmin
                wmax = fractal[x][y] if fractal[x][y] > wmax else wmax

        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                # this model goes from cold(top) -> hot(bottom)'
                #                        0.0->1.0               0 -> 1
                self.heat[x][y] = self.heat[x][y] * norm(fractal[x][y], float(wmin), float(wmax))
                mini = self.heat[x][y] if self.heat[x][y] < mini else mini
                maxa = self.heat[x][y] if self.heat[x][y] > maxa else maxa

        for i in range(len(self.heat)):
            for j in range(len(self.heat[0])):
                self.heat[i][j] = norm(self.heat[i][j], mini, maxa)
        return mini, maxa

    def applyHeight(self, height):
        def norm(x, mina, maxi):
            return ((x-mina)/(maxi-mina))
        def val(x, y): 
            return x*y
        copy = numpy.copy(self.heat)
        mini, maxa = 0, 0
        hmin, hmax = 0, 0
        for x in range(len(height)):
            for y in range(len(height[0])):
                hmin = height[x][y] if height[x][y] < hmin else hmin
                hmax = height[x][y] if height[x][y] > hmax else hmax

        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                if val(.98, 255) <= height[x][y]:
                    self.heat[x][y] -= (height[x][y]/255.0) * .2
                elif val(.78, 255) <= height[x][y] < val(.98, 255):
                    self.heat[x][y] -= (height[x][y]/255.0) * .25
                elif val(.49, 255) <= height[x][y] < val(.78, 255):
                    self.heat[x][y] -= (height[x][y]/255.0) * .3
                elif val(.39, 255) <= height[x][y] < val(.49, 255):
                    self.heat[x][y] -= (height[x][y]/255.0) * .35
                else:
                    self.heat[x][y] -= (height[x][y]/255.0) *.4
                mini = self.heat[x][y] if self.heat[x][y] < mini else mini
                maxa = self.heat[x][y] if self.heat[x][y] > maxa else maxa
        for i in range(len(self.heat)):
            for j in range(len(self.heat[0])):
                self.heat[i][j] = norm(self.heat[i][j], mini, maxa)
                if 0 <= self.heat[i][j]< val(.4, maxa):
                    copy[i][j] = 0
                elif val(0.4, maxa) <= self.heat[i][j]< val(.6, maxa):
                    copy[i][j] = 1
                elif val(0.6, maxa) <= self.heat[i][j]< val(.75, maxa):
                    copy[i][j] = 2
                elif val(0.75, maxa) <= self.heat[i][j]< val(.85, maxa):
                    copy[i][j] = 3
                elif val(0.85, maxa) <= self.heat[i][j]< val(.95, maxa):
                    copy[i][j] = 4
                else:
                    copy[i][j] = 5
        return mini, maxa, copy