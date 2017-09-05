import random
import pprint
import numpy

class MPD:
    def __init__(self, width, height, roughness):
        # 2D list initialized using row major
        self.width = width
        self.height = height
        print(width, height)
        self.min = 125
        self.max = 125
        self.map = [[0 for j in range(height+1)] for i in range(width+1)]
        self.noise = roughness
        self.initialize()

    def randvalue(self):
        return random.random()*2-1

    def normalize(self, x):
        """ clamp between -1 and 1 """
        return max(-1, min(x, 1))

    def displace(self, width, height):
        h, w, n, r = self.height, self.width, self.noise, self.randvalue()
        return (width+height)/(h+w)*n*r

    def minmax(self, x):
        self.min = x if x < self.min else self.min
        self.max = x if x > self.max else self.max
        return x

    def colorize(self):
        for i in range(self.height+1):
            for j in range(self.width+1):
                self.map[j][i] = self.minmax(int(round(((self.map[j][i]+1)/2)*255)))
                
    def initialize(self):
        # # # # # #
        # a  b  c #
        # d  e  f #
        # g  h  i #
        # # # # # #

        # get map dimensions shifted by 1 to account for map indices
        W, H = self.width, self.height
        # initialize cornersq
        self.map[0][0] = a = self.randvalue()
        self.map[W][0] = c = self.randvalue()
        self.map[0][H] = g = self.randvalue()
        self.map[W][H] = i = self.randvalue()

        # initialize diamond
        self.map[W//2][0] = b = (a+c)/2+self.displace(W,H)
        self.map[0][H//2] = d = (a+g)/2+self.displace(W,H)
        self.map[W][H//2] = f = (c+i)/2+self.displace(W,H)
        self.map[W//2][H] = h = (g+i)/2+self.displace(W,H)

        # initialize square
        self.map[W//2][H//2] = e = self.normalize((b+d+f+h)/4)

        # recursive call
        self.midpoints((0,0), (W//2, H//2))
        self.midpoints((W//2,0), (W, H//2))
        self.midpoints((0,H//2), (W, H//2))
        self.midpoints((W//2,H//2), (W, H))

    def midpoints(self, a, i):
        print(a, i)
        ax, ay = a
        ix, iy = i
        ax, ay = int(ax), int(ay)
        ix, iy = int(ix), int(iy)
        cx, cy = int(ix), int(ay)
        gx, gy = int(ax), int(iy)
        
        if ax+1 >= ix or ay+1 >= iy:
            return

        a = self.map[ax][ay]
        c = self.map[cx][cy]
        g = self.map[gx][gy]
        i = self.map[ix][iy]

        W, H = (ix+ax)//2, (iy+ay)//2
        print(W,H)
        # initialize diamond
        self.map[W][ay] = b = (a+c)/2+self.displace(W,H)
        self.map[ax][H] = d = (a+g)/2+self.displace(W,H)
        self.map[W][iy] = f = (c+i)/2+self.displace(W,H)
        self.map[ix][H] = h = (g+i)/2+self.displace(W,H)

        # initialize square
        self.map[W][H] = e = self.normalize((b+d+f+h)/4)

        # recursive call
        self.midpoints((ax,ay), (ix-W//2, iy-H//2))
        self.midpoints((ix-W//2,ay), (ax+W, ay+H//2))
        self.midpoints((ax+0,ax+H//2), (ax+W//2, ax+H))
        self.midpoints((W//2,H//2), (W, H))
        

if __name__ == "__main__":
    SIZE = 16
    mpd = MPD(SIZE, SIZE, .55)
    mpd.colorize()
    print(numpy.matrix(mpd.map))
    print([int(round(((mpd.displace(16,16)+1)/2)*255)) for i in range(100)])
