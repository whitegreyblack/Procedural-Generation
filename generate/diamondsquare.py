import math
import random
from color import Color
from header import line
from copy import deepcopy
from pprint import pprint
from PIL import Image, ImageDraw
from collections import namedtuple
from combinations import Sequences
from bearlibterminal import terminal as term

Point = namedtuple("Point", "x y")
Box = namedtuple("Box", "x1 y1 x2 y2")

def print_term(map, size):
    term.open()
    s = 2 ** size + 1
    term.set(f'window: title=DiamondSquare, size={s}x{s}, cellsize=8x8')

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            term.puts(x, y, "[c={}]#[/c]".format(cell))

    term.refresh()
    term.read()

def print_image(map, size, pid='0'):    
    s = 2 ** size + 1
    img = Image.new('RGB', (s, s))
    ids = ImageDraw.Draw(img)

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            # ids.point([x, y, x+1, y+1], cell)
            ids.rectangle([x, y, x , y], cell)

    img_name = 'diamond_square_{}.png'.format(pid)
    img.save('../pics/' + img_name)    

class DSW:
    LAND ="#008855"
    WATER = "#005577"
    def __init__(self, power, noise=.5, delta=.8):
        size = 2 ** power + 1
        print(size, size * size)
        self.width, self.height = size, size
    
        # initialize to zero
        self.map = [[0.0 for j in range(size)] for i in range(size)]
        self.hex = [[0.0 for j in range(size)] for i in range(size)]
        self.clr = [[0.0 for j in range(size)] for i in range(size)]

        self.noise = noise
        self.delta = delta
        self.run()

        self.normalize()

    def prettify(self):
        def fmtfloat(x):
            return "{:6.2f}".format(x)

        for row in self.map:
            print(" ".join(map(fmtfloat, row)))

    def random_float(self):
        return random.random() * 2 - 1

    def random_range(self, a, b):
        return random.uniform(a, b)

    def random_clamp(self):
        return random.random()

    def at(self, x, y):
        return self.map[y][x]

    def set(self, x, y, v):
        # print(f'x={x:3}, y={y:3}, v={v:5.2f}')
        self.map[y][x] = v

    def minimize(self):
        if not hasattr(self, 'min'):
            self.min = min(cell for row in self.map for cell in row)
        
        return self.min
            
    def maximize(self):
        if not hasattr(self, 'max'):
            self.max = max(cell for row in self.map for cell in row)

        return self.max

    def normalize(self):
        min = self.minimize()
        max = self.maximize()

        self.values = []

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.map[y][x] = (cell - min) / (max - min)
                self.values.append(self.map[y][x])

        sorted(self.values)
        self.divide()

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.hex[y][x] = self.float_to_hex(cell)
                self.clr[y][x] = self.float_to_clr(cell)

    def sort_array_max(self):
        def distance(i, j):
            x = (self.width // 2) - i
            y = (self.height // 2) - j
            return math.sqrt((x * x) + (y * y))

        maxes = sorted([(x, i, j) 
            for j, y in enumerate(self.map) 
                for i, x in enumerate(y)], 
            reverse=True,
            key=lambda x: (x[0], distance(x[1], x[2])))

        print(maxes[0], maxes[1])
        
        for x, y in line((maxes[0][1:]), maxes[1][1:]):
            self.map[y][x] = "#4433AA"

    def divide(self):
        self.mountains = round(self.width * self.height * .99)
        self.forests = round(self.width * self.height * .8)
        self.grassland = round(self.width * self.height * .55)
        print(self.mountains, self.forests, self.grassland)

    def float_to_clr(self, x):

        if x > self.values[self.grassland]:
            return self.LAND

        # elif self.values[self.forests] <= x < self.values[self.mountains]:
        #     return "#000000"

        # elif x > self.values[self.grassland]:
        #     return "#008855"

        else:
            return self.WATER

    def float_to_hex(self, x):
        value = hex(round(x * 250)).split('x')[1]
        
        if len(value) < 2:
            value = '0' + value

        return '#' + value * 3

    def run(self):
        b = Box(0, 0, self.width - 1, self.height - 1)

        # initialize corners
        self.set(b.x1, b.y1, self.random_float())
        self.set(b.x1, b.y2, self.random_float())
        self.set(b.x2, b.y1, self.random_float())
        self.set(b.x2, b.y2, self.random_float())

        self.diamondsquare(b, self.delta)

    def diamondsquare(self, box, noise):
        hx, hy = (box.x2 - box.x1) // 2, (box.y2 - box.y1) // 2

        # b = [
        #     [(box.x1, box.y1), (box.x1 + hx, box.y1), (box.x2, box.y1)],
        #     [(box.x1, box.y1 + hy), (box.x1 + hx, box.y1 + hy), (box.x2, box.y1 + hy)],
        #     [(box.x1, box.y2), (box.x1 + hx, box.y2), (box.x2, box.y2)],
        # ]
        # print('-- box --')
        # for points in b:
        #     print(", ".join((map(lambda xy: "({}, {})".format(xy[0], xy[1]), points))))

        p5 = Point(box.x1 + hx, box.y1 + hy)
        
        p7 = self.at(box.x1, box.y1)
        p1 = self.at(box.x1, box.y2)
        p9 = self.at(box.x2, box.y1)
        p3 = self.at(box.x2, box.y2)

        self.set(p5.x, p5.y, ((p1 + p3 + p7 + p9) / 4) + self.random_range(-noise, noise))
        
        p5 = self.at(p5.x, p5.y)

        x2, y2 = box.x1 + hx, box.y2	
        x4, y4 = box.x1, box.y1 + hy
        x6, y6 = box.x2, box.y1 + hy
        x8, y8 = box.x1 + hx, box.y1

        self.set(x2, y2, ((p1 + p3 + p5) / 3) + self.random_range(-noise, noise))
        # self.set(x4, y4, ((p1 + p5 + p7) / 3) + self.random_range(-noise, noise))
        self.set(x6, y6, ((p3 + p5 + p9) / 3) + self.random_range(-noise, noise))
        # self.set(x8, y8, ((p5 + p7 + p9) / 3) + self.random_range(-noise, noise))

        # noise = noise * (2 ** -.75)
        noise /= 2 ** self.noise

        # print(noise)
        if box.x2 - box.x1 > 2 or box.y2 - box.y1 > 2:
            self.diamondsquare(Box(
                box.x1, box.y1, 
                box.x1 + hx, box.y1 + hy), noise)

            self.diamondsquare(Box(
                box.x1 + hx, box.y1,
                box.x2, box.y1 + hy), noise)

            self.diamondsquare(Box(
                box.x1, box.y1 + hy,
                box.x1 + hx, box.y2), noise)

            self.diamondsquare(Box(
                box.x1 + hx, box.y1 + hy, 
                box.x2, box.y2), noise)

    def remove_singles(self):
        '''Removes isolated land or water tiles'''
        new_map = deepcopy(self.clr)

        for j, y in enumerate(self.clr):
            for i, x in enumerate(y):
                remove = True
                for ii, jj in Sequences.sequences(Sequences.ALL):
                    try:
                        if self.clr[j+jj][i+ii] == x:
                            remove = False
                            break

                    except IndexError:
                        pass

                if remove:
                    print('removing', i, j)
                    new_map[j][i] = self.WATER if x == self.LAND else self.LAND

        self.clr = deepcopy(new_map)

if __name__ == "__main__":
    seed = random.randint(0, 99999)
    print(seed)
    random.seed(seed)
    size = 3
    # dsw = DSW(size, noise=.72, delta=.8)
    # dsw.prettify()
    # term_print(dsw.hex, 6)
    # norm_print(dsw.hex, size, pid='0')

    dsw = DSW(size, noise=.55, delta=.65)
    print_image(dsw.clr, size, pid='2n')
    dsw.sort_array_max()
    dsw.remove_singles()
    print_image(dsw.hex, size, pid='1n')
    print_image(dsw.clr, size, pid='1c')
    # norm_print(dsw.hex, size, pid='1n')
    # color_print(dsw.clr, size, pid='1c')

    # heat = DSW(size, noise=.55, delta=.65)