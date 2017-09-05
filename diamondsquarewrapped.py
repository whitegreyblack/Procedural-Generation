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

    def rand(self):
        return random.random()*2-1

    def getsample(self, x, y):
        return self.map[x&self.width-1][y&self.height-1]

    def setsample(self, x, y, z):
        self.map[x&self.width-1][y&self.height-1] = z

    def minmax(self, x):
        return x

    def colorize(self):
        for i in range(self.height):
            for j in range(self.width):
                self.map[j][i] = self.minmax(int((self.map[j][i]+1.0)/2.0*255))

    def norm(self, x):
        """ clamp between -1 and 1 """
        return max(-1, min(x, 1))

    def normeAll(self):
        for i in range(self.width):
            for j in range(self.height):
                self.map[i][j] = self.norm(self.map[i][j])

    def initialize(self):

        # get map dimensions shifted by 1 to account for map indices
        W, H = self.width, self.height
        # initialize corners
        self.map[0][0] = self.rand()
        self.map[0][0] = self.rand()
    
    def square(self, x, y, size, value):
        pass

    def diamondsquare(self, width, height):
        q4 = (0, 0, width/2, height/2)
        q1 = (width/2, 0, width, height/2)
        q2 = (width/2, height/2, width, height)
        q3 = (0, height/2, width/2, height)
        print(q4)
        print(q1)
        print(q2)
        print(q3)

        # # initialize square
        # self.map[W/2][H/2] = e = (a+c+g+i)/4

        # # initialize diamond
        # self.map[W/2][0] = b = (a+c+e+e)/4
        # self.map[0][H/2] = d = (a+g+e+e)/4
        # self.map[W][H/2] = f = (c+i+e+e)/4
        # self.map[W/2][H] = h = (a+c+e+e)/4

        # # recursive call
        # #self.diamondsquare(W, H)
