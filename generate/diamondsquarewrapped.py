import random
from collections import namedtuple
from pprint import pprint
from bearlibterminal import terminal as term
from PIL import Image, ImageDraw

Point = namedtuple("Point", "x y")
Box = namedtuple("Box", "x1 y1 x2 y2")

class DSW:
    def __init__(self, power, roughness=.5):
        size = 2 ** power + 1
        print(size)
        self.width, self.height = size, size
        self.min = 125
        self.max = 125

        # initialize to zero
        self.map = [[0.0 for j in range(size)] for i in range(size)]
        self.hex = [[0.0 for j in range(size)] for i in range(size)]

        self.noise = roughness
        self.run()

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
        # print(x, y, self.map[y][x])
        return self.map[y][x]

    def set(self, x, y, v):
        # print(f'x={x:3}, y={y:3}, v={v:5.2f}')
        self.map[y][x] = v

    def minimize(self):
        return min(cell for row in self.map for cell in row)
        
    def maximize(self):
        return max(cell for row in self.map for cell in row)

    def normalize(self):
        """ clamp between -1 and 1 """
        min = self.minimize()
        max = self.maximize()
        print(max, min)

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.map[y][x] = (cell - min) / (max - min)
                self.hex[y][x] = self.float_to_hex(self.map[y][x])

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

        self.diamondsquare(b, .75)

        self.normalize()

    def breadthfirst(self, box, noise):
        pass

    def diamondsquare(self, box, noise):
        hx, hy = (box.x2 - box.x1) // 2, (box.y2 - box.y1) // 2
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
        self.set(x4, y4, ((p1 + p5 + p7) / 3) + self.random_range(-noise, noise))
        self.set(x6, y6, ((p3 + p5 + p9) / 3) + self.random_range(-noise, noise))
        self.set(x8, y8, ((p5 + p7 + p9) / 3) + self.random_range(-noise, noise))

        # noise = noise * (2 ** -.75)
        noise *= 2 ** -.75

        print(noise)
        if box.x2 - box.x1 > 2 or box.y2 - box.y1 > 2:
            self.diamondsquare(Box(
                box.x1, box.y1, 
                box.x1 + hx, box.y1 + hy), noise)

            self.diamondsquare(Box(
                box.x1, box.y1 + hy,
                box.x1 + hx, box.y2), noise)

            self.diamondsquare(Box(
                box.x1 + hx, box.y1,
                box.x2, box.y1 + hy), noise)

            self.diamondsquare(Box(
                box.x1 + hx, box.y1 + hy, 
                box.x2, box.y2), noise)

def term_print(map, size):
    term.open()
    s = 2 ** size + 1
    term.set(f'window: title=DiamondSquare, size={s}x{s}, cellsize=8x8')

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            term.puts(x, y, "[c={}]#[/c]".format(cell))

    term.refresh()
    term.read()

def img_print(map, size):
    s = 2 ** size + 1
    img = Image.new('RGB', (s, s))
    ids = ImageDraw.Draw(img)

    for y, row in enumerate(map):
        for x, cell in enumerate(row):
            # ids.point([x, y, x+1, y+1], cell)
            ids.rectangle([x, y, x + 1, y + 1], cell)

    img_name = 'diamond_square.png'
    img.save('../pics/' + img_name)        

if __name__ == "__main__":
    size = 7
    dsw = DSW(size, roughness=.72)
    # dsw.prettify()
    # term_print(dsw.hex, 6)
    img_print(dsw.hex, size)