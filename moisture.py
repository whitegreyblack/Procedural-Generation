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

class MM:
    def __init__(self, world):
        self.size = len(world)
        self.rain = [[world[x][y]/255.0 for y in range(self.size)] for x in range(self.size)]

    def vanilla(self):
        mini, maxa = 0, 0
        for x in range(len(self.rain)):
            for y in range(len(self.rain[0])):
                mini = self.rain[x][y] if self.rain[x][y] < mini else mini
                maxa = self.rain[x][y] if self.rain[x][y] > maxa else maxa
        return mini, maxa

    def applyHeight(self, height):
        def norm(x, mina, maxi):
            return ((x-mina)/(maxi-mina))
        def val(x, y): 
            return x*y
        copy = numpy.copy(self.rain)
        mini, maxa = 0, 0
        hmin, hmax = 0, 0
        for x in range(len(height)):
            for y in range(len(height[0])):
                hmin = height[x][y] if height[x][y] < hmin else hmin
                hmax = height[x][y] if height[x][y] > hmax else hmax

        for x in range(len(self.rain)):
            for y in range(len(self.rain[0])):
                if val(.98, 255) <= height[x][y]:
                    self.rain[x][y] += (height[x][y]/255.0) * .4
                elif val(.78, 255) <= height[x][y] < val(.98, 255):
                    self.rain[x][y] += (height[x][y]/255.0) * .25
                elif val(.49, 255) <= height[x][y] < val(.78, 255):
                    self.rain[x][y] += (height[x][y]/255.0) * .3
                elif val(.39, 255) <= height[x][y] < val(.49, 255):
                    self.rain[x][y] += (height[x][y]/255.0) * .35
                mini = self.rain[x][y] if self.rain[x][y] < mini else mini
                maxa = self.rain[x][y] if self.rain[x][y] > maxa else maxa

        for i in range(len(self.rain)):
            for j in range(len(self.rain[0])):
                self.rain[i][j] = norm(self.rain[i][j], mini, maxa)
                if 0 <= self.rain[i][j]< val(.4, maxa):
                    copy[i][j] = 5
                elif val(0.4, maxa) <= self.rain[i][j]< val(.6, maxa):
                    copy[i][j] = 4
                elif val(0.6, maxa) <= self.rain[i][j]< val(.75, maxa):
                    copy[i][j] = 3
                elif val(0.75, maxa) <= self.rain[i][j]< val(.85, maxa):
                    copy[i][j] = 2
                elif val(0.85, maxa) <= self.rain[i][j]< val(.95, maxa):
                    copy[i][j] = 1
                else:
                    copy[i][j] = 0
        return mini, maxa, copy