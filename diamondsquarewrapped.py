import random

class DSW:
    def __init__(self, width, height, roughness):
        self.width = width
        self.height = height
        self.min = 125
        self.max = 125
        self.map = [[0 for j in range(height)] for i in range(width)]
        self.noise = roughness
        self.initialize()

    def randvalue(self):
        return random.random()*2-1

    def minmax(self, x):
        return x

    def colorize(self):
        for i in range(self.height):
            for j in range(self.width):
                self.map[j][i] = self.minmax(int(round(((self.map[j][i]+1)/2)*255)))

    def normalize(self, x):
        """ clamp between -1 and 1 """
        return max(-1, min(x, 1))

    def normalizeAll(self):
        for i in range(self.width):
            for j in range(self.height):
                self.map[i][j] = self.normalize(self.map[i][j])

    def initialize(self):

        # get map dimensions shifted by 1 to account for map indices
        W, H = self.width-1, self.height-1
        rand = self.randvalue()
        # initialize corners
        self.map[0][0] = a = rand
        self.map[W][0] = c = rand
        self.map[0][H] = g = rand
        self.map[W][H] = i = rand

        # initialize square
        self.map[W/2][H/2] = e = (a+c+g+i)/4

        # initialize diamond
        self.map[W/2][0] = b = (a+c+e+e)/4
        self.map[0][H/2] = d = (a+g+e+e)/4
        self.map[W][H/2] = f = (c+i+e+e)/4
        self.map[W/2][H] = h = (a+c+e+e)/4

        # recursive call
        self.diamondsquare(W, H)