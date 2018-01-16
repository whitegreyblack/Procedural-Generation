import random
from collections import namedtuple

point = namedtuple("Point", "x y")
box = namedtuple("Box", "x1 y1 x2 y2")

class DSW:
    def __init__(self, power, roughness):
        size = 2 ** power + 1
        print(size)
        self.width, self.height = size, size
        self.min = 125
        self.max = 125

        # initialize to zero
        self.map = [[0.0 for j in range(size)] for i in range(size)]

        self.noise = roughness
        self.initialize()

    def random_float(self):
        return random.random() * 2 - 1

    def at(self, x, y):
        return self.map[y][x]

    def set(self, x, y, v):
	self.map[y][x] = v

    def norm(self, x):
        """ clamp between -1 and 1 """
        return max(-1, min(x, 1))

    def initialize(self):
        # get map dimensions shifted by 1 to account for map indices
        b = box(0, 0, self.width - 1, self.height - 1)

        print(b)

        # initialize corners
        self.map[b.y1][b.x1] = self.random_float() 
        self.map[b.y1][b.x2] = self.random_float()
        self.map[b.y2][b.x1] = self.random_float()
        self.map[b.y2][b.x1] = self.random_float()

        # once
        self.diamond(b)

        # four times
        self.square(b)

    def diamond(self, box):
        x5, y5 = box.x2 // 2, box.y2 // 2
        
        p1 = self.at(box.x1, box.y2)
        p3 = self.at(box.x2, box.y2)
        p7 = self.at(box.x1, box.y1)
        p9 = self.at(box.x2, box.y1)

        self.set(x5, y5, (p1 + p3 + p7 + p9) / 4)

    def square(self, box):
        p1 = self.at(box.x1, box.y2)
        p3 = self.at(box.x2, box.y2)
	p5 = self.at(box.x2 // 2, box.y2 // 2)
        p7 = self.at(box.x1, box.y1)
        p9 = self.at(box.x2, box.y1)

	x2, y2 = box.x2 // 2, box.y2	
        self.set(x2, y2, (p1 + p3 + p5 / 3))

	x4, y4 = box.x1, box.y2 // 2
	self.set(x4, y4, (p1 + p5 + p3 / 3))

        x6, y6 = box.x2, box.y2 // 2
	self.set(x6, y6, (p3 + p5 + p9 / 3))

        x8, y8 = box.x2 // 2, box.y1
	self.set(x8, y8, (p5 + p7 + p9 / 3))
	
if __name__ == "__main__":
    dsw = DSW(5, .5)
    print(dsw.map) 
