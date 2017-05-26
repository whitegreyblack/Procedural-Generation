import random
import pprint
import numpy

class MPD:
    def __init__(self, width, height, roughness):
        # 2D list initialized using row major
        self.width = width
        self.height = height
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

        # get map dimensions shifted by 1 to account for map indices
        W, H = self.width, self.height

        # initialize corners
        self.map[0][0] = a = self.randvalue()
        self.map[W][0] = c = self.randvalue()
        self.map[0][H] = g = self.randvalue()
        self.map[W][H] = i = self.randvalue()

        # initialize square
        self.map[W/2][H/2] = e = self.normalize((a+c+g+i)/4)

        # initialize diamond
        self.map[W/2][0] = b = (a+c+e+e)/4
        self.map[0][H/2] = d = (a+g+e+e)/4
        self.map[W][H/2] = f = (c+i+e+e)/4
        self.map[W/2][H] = h = (a+c+e+e)/4

        # recursive call
        self.diamondsquare(W, H)
    
    def diamondsquare(self, width, height):

        if not width/2 > 1:
            return
        if not height/2 > 1:
            return
        for x in range(width/2, self.width+1, width/2):
            for y in range(height/2, self.height+1, height/2):
                a = self.map[x-width/2][y-height/2]
                c = self.map[x][y-height/2]
                g = self.map[x-width/2][y]
                i = self.map[x][y]

                # square step
                self.map[x-width/4][y-height/4] = e = self.normalize((a+c+g+i)/4+self.displace(width, height))

                # diamond N
                if(y-height+(height/4) > 0):
                    n = self.map[x-(width/4)][y-height+(height/4)]
                    self.map[x-(width/4)][y-height/2] = self.normalize((a+c+e+n)/4+self.displace(width, height))
                else:
                    self.map[x-(width/4)][y-height/2] = self.normalize((a+c+e)/3+self.displace(width, height))

                # diamond S
                if(y+(height/4) < self.height):
                    n = self.map[x-(height/4)][y+(height/4)]
                    self.map[x-width/4][y] = self.normalize(g+i+e+n)/4+self.displace(width, height)
                else:
                    self.map[x-width/4][y] = self.normalize(g+i+e)/3+self.displace(width, height)
        
                # diamond W
                if(x-width+(width/4) > 0):
                    n = self.map[x-width+(width/4)][y-(height/4)]
                    self.map[x-width/2][y-height/4] = self.normalize((a+g+e+n)/4+self.displace(width, height))
                else:
                    self.map[x-width/2][y-height/4] = self.normalize((a+g+e)/3+self.displace(width, height))

                # diamond E
                if(x+(width/4) < self.width):
                    n = self.map[x+width/4][y-height/4]
                    self.map[x][y-height/4] = self.normalize((c+i+e+n)/4+self.displace(width, height))
                else:
                    self.map[x][y-height/4] = self.normalize((c+i+e)/3+self.displace(width, height))

        self.diamondsquare(width/2, height/2)

if __name__ == "__main__":
    SIZE = 16
    mpd = DSA(SIZE, SIZE, .55)
    mpd.colorize()
    print(numpy.matrix(mpd.map))