from PIL import Image, ImageDraw
from bearlibterminal import terminal
from mpd_one_dim import key_handle_exit, setup
import math
import color
from random import choice, randint, random
"""
52666 40 20
21096 100 80
56330 100 80
"""

def steps_4_way():
    steps = set()
    for i in range(-1, 2, 2):
        steps.add((0, i))
        steps.add((i, 0))
    return steps

def steps_8_way():
    steps = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                steps.add((i, j))
    return steps

def steps_9_way():
    steps = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            steps.add((i, j))
    return steps

''' map functions '''
class Map:
    def __init__(self, width, height, limit, seed=None):
        self.x, self.y = width, height
        self.limit = int(height * width * limit)
        self.world = [[0 for _ in range(width)] for _ in range(height)]
        self.seed = randint(0, 99999) if not seed else seed
        self.build()

    def check_bounds(self, x, y):
        return 0 <= x < self.x and 0 <= y < self.y

    def random_point(self):
        return randint(0, self.x -1), randint(0, self.y - 1)

    def neighbors(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_9_way()]
     
    def smooth(self):
        world = [[0 for _ in range(self.x)] for _ in range(self.y)]
        for y in range(self.y):
            for x in range(self.x):
                num = 0
                value = 0
                for xx, yy in self.neighbors(x, y):
                    try:
                        value += self.world[yy][xx]
                        num += 1
                    except IndexError:
                        pass

                world[y][x] = value/num
        self.world = world

    def build(self, seed=None): 
        """ Returns map filled with drunkards height algo """
        self.spaces = set()
        steps = steps_4_way()
        ry, rx = self.random_point()

        while len(self.spaces) <= self.limit:
            step = choice(list(steps))
            # if at somepoint we are at the edge of the map and choose
            # a point outside of the map bounds we choose a random point
            # from the map to start the process again
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        # Can smooth more than once but each smooth makes the terrain
        # flatter and flatter
        self.smooth()

        # This double for loop puts all heights into the height set
        # for evaluation and analysis purposes
        # We do this after for loop so it doesn't hold every single 
        # number possible starting from 0
        height = set()
        for y in range(self.y):
            for x in range(self.x):
                if self.world[y][x] not in height:
                    height.add(self.world[y][x])

        self.z = sorted(height, reverse=True)[0]
        self.evaluate()

    def split_range(self, number=10):
        if not hasattr(self, 'z'):
            raise AttributeError("Map not built yet -- call build()")

        return sorted([(self.z * i) // number for i in range(10)], reverse=True)

    def integer_to_hex(self, value):
        value = hex(value).split('x')[1]
        if len(value) < 2:
            value = "0" + value
        return '#' + value * 3

    def normalize(self, value):
        return int((value / self.z) * 250)

    def evaluate(self):
        if not hasattr(self, 'z'):
            raise AttributeError("Map not built yet -- call build()")

        self.world_normal = [[0 for _ in range(self.x)] for _ in range(self.y)]
        self.world_colored = [[0 for _ in range(self.x)] for _ in range(self.y)]

        ranges = self.split_range()
        a, b, c, d = 2, 5, 7, 8
        
        for y in range(self.y):
            for x in range(self.x):
                if self.world[y][x] >= ranges[a]:
                    self.world_colored[y][x] = ('A', '#FFFFFF')
                    self.world_normal[y][x] = ('A', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[b] <= self.world[y][x] < ranges[a]:
                    self.world_colored[y][x] = ('n', '#808080')
                    self.world_normal[y][x] = ('A', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[c] <= self.world[y][x] < ranges[b]:
                    self.world_colored[y][x] = ('*', '#40FF40')
                    self.world_normal[y][x] = ('*', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[d] <= self.world[y][x] < ranges[c]:
                    self.world_colored[y][x] = ('.', '#80FF80')
                    self.world_normal[y][x] = ('.', self.integer_to_hex(self.normalize(self.world[y][x])))

                else:
                    self.world_colored[y][x] = ('~', '#4040FF')
                    self.world_normal[y][x] = ('~', self.integer_to_hex(self.normalize(self.world[y][x])))

    def output_terminal(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        for y in range(self.y):
            for x in range(self.x):
                yield (x, y, *world[y][x])

    def output_image(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        img = Image.new('RGB', (self.x * 8, self.y * 8))
        ids = ImageDraw.Draw(img)
        for y in range(self.y):
            for x in range(self.x):
                ids.rectangle(
                    [x * 8, y * 8, x * 8 + 8, y * 8 + 8], world[y][x][1])
        img.save('drunkards.png')

if __name__ == "__main__":
    width, height = 160, 50
    setup(width, height)
    m = Map(width, height, .3)
    m.build()
    output_flag = 1
    while True:
        # console.clear()
        terminal.clear()
        for x, y, ch, col in list(m.output_terminal()):
            terminal.puts(x, y, '[c={}]{}[/c]'.format(col, ch))
        terminal.refresh()

        key = terminal.read()
        if key_handle_exit(key):
            break
        elif key == terminal.TK_F:
            output_flag *= -1
            if output_flag > 0:
                method = m.output()
            else:
                method = m.output_color()
