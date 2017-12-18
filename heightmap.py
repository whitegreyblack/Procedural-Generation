from bearlibterminal import terminal
from mpd_one_dim import key_handle_exit, setup
import math
import color
from random import choice, randint, random
import randomfill
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

''' map functions '''
class Map:
    def __init__(self, width, height, limit, seed=None):
        self.x, self.y = width, height
        self.limit = int(height * width * limit)
        self.world = [[0 for _ in range(width)] for _ in range(height)]
        self.seed = randint(0, 99999) if not seed else seed
        print(self.limit)

    def check_bounds(self, x, y):
        return 0 <= x < self.x and 0 <= y < self.y

    def random_point(self):
        return randint(0, self.x -1), randint(0, self.y - 1)

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

    def evaluate(self):
        if not hasattr(self, 'z'):
            raise AttributeError("Map not built yet -- call build()")

        self.world_normal = [[0 for _ in range(self.x)] for _ in range(self.y)]
        self.world_colored = [[0 for _ in range(self.x)] for _ in range(self.y)]

        self.world_normal[0][0] = 5
        print(self.world_colored[0][0])
        ranges = self.split_range()
        print(ranges)
        for y in range(self.y):
            for x in range(self.x):
                if self.world[y][x] >= ranges[0]:
                    self.world_normal[y][x] = ('A', '#FFFFFF')
                    self.world_colored[y][x] = ('A', '#FFFFFF')

                elif ranges[1] <= self.world[y][x] < ranges[0]:
                    self.world_colored[y][x] = ('n', '#808080')
                    self.world_normal[y][x] = ('n', '#FFFFFF')

                elif ranges[4] <= self.world[y][x] < ranges[1]:
                    self.world_colored[y][x] = ('*', '#40FF40')
                    self.world_normal[y][x] = ('*', '#FFFFFF')

                elif ranges[8] <= self.world[y][x] < ranges[4]:
                    self.world_colored[y][x] = ('.', '#40FF40')
                    self.world_normal[y][x] = ('.', '#FFFFFF')

                else:
                    self.world_colored[y][x] = ('~', '#4040FF')
                    self.world_normal[y][x] = ('~', '#FFFFFF')

    def output(self):
        for y in range(self.y):
            for x in range(self.x):
                yield (x, y, *self.world_normal[y][x])

    def output_color(self):
        for y in range(self.y):
            for x in range(self.x):
                yield (x, y, *self.world_colored[y][x])

if __name__ == "__main__":
    width, height = 160, 50
    setup(width, height)
    m = Map(width, height, .3)
    m.build()
    output_flag = 1
    while True:
        # console.clear()
        terminal.clear()
        for x, y, ch, col in list(m.output_color()):
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
