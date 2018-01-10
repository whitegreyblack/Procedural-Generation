import random

class DSW:
    def __init__(self, width, height, roughness):
        self.width = width
        self.height = height
        self.min = 125
        self.max = 125
        self.map = [[random.random() * 2 - 1 for j in range(height)] for i in range(width)]
        self.noise = roughness
        self.initialize()

    def rand(self):
        return random.random()*2-1

    def get(self, x, y):
        return self.map[x % self.width - 1][y % self.height - 1]

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
        xs, ys = 0, 0
        xm, ym = width // 2, height // 2
        xe, ye = width, height
        print('BEG: ', xs, ys)
        print('MID: ', xm ,ym)
        print('END: ', xe, ye)
        q4 = (xs, ys, xm, ym)
        q1 = (xm, ys, xe, ym)
        q2 = (xm, ym, xe, ye)
        q3 = (xs, ym, xm, ye)
        print(q4, q1)
        print(q3, q2)
        # initialize square
        # self.map[width//2][height//2] = e = (self.get() + c + g + i) / 4

        # # initialize diamond
        # self.map[W/2][0] = b = (a+c+e+e)/4
        # self.map[0][H/2] = d = (a+g+e+e)/4
        # self.map[W][H/2] = f = (c+i+e+e)/4
        # self.map[W/2][H] = h = (a+c+e+e)/4

        # # recursive call
        # #self.diamondsquare(W, H)

if __name__ == "__main__":
    dsw = DSW(200, 50, .5)
    dsw.diamondsquare(dsw.width, dsw.height)
    