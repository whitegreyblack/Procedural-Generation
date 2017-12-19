import math
import color
import random
from random import randint, choice
import randomfill
from drunkards import setup, key_handle_exit, steps_4_way
from bearlibterminal import terminal

''' map functions '''
class Map:
    def __init__(self, x, y, l, peaks, seed=None):
        """Drunkards algorithm with peaks"""
        self.seed = seed if seed else random.randint(0, 9999)
        random.seed(self.seed)

        self.x, self.y = x, y
        self.limit = int(x * y * l)
        self.world = [[0 for _ in range(x)] for _ in range(y)]
        self.peaks = [(
            randint(x // 2 - x // 4, x // 2 + x // 4), 
            randint(y // 2 - y // 3, y // 2 + y // 3)) 
                for _ in range(peaks)]

    def check_bounds(self, x, y):
        return 0 <= x < self.x and 0 <= y < self.y

    def random_point(self):
        # return randint(0, self.x -1), randint(0, self.y - 1)
        return self.peaks[randint(0, len(self.peaks) - 1)]

    def generate(self):
        self.spaces = set()
        rx, ry = self.random_point()
        while len(self.spaces) <= self.limit:
            step = choice(list(steps_4_way()))
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

    def maxa(self):
        height = set()
        for y in range(self.y):
            for x in range(self.x):
                if self.world[y][x] not in height:
                    height.add(self.world[y][x])

        self.z = sorted(height, reverse=True)[0]

    def integer_to_hex(self, value):
        value = hex(value).split('x')[1]
        if len(value) < 2:
            value = "0" + value
        return '#' + value * 3

    def split_range(self, number=10):
        if not hasattr(self, 'z'):
            raise AttributeError("Map not built yet -- call build()")

        return sorted([(self.z * i) // number for i in range(10)], reverse=True)

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
                    self.world_normal[y][x] = ('^', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[b] <= self.world[y][x] < ranges[a]:
                    self.world_colored[y][x] = ('n', '#808080')
                    self.world_normal[y][x] = ('^', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[c] <= self.world[y][x] < ranges[b]:
                    self.world_colored[y][x] = ('*', '#40FF40')
                    self.world_normal[y][x] = ('*', self.integer_to_hex(self.normalize(self.world[y][x])))

                elif ranges[d] <= self.world[y][x] < ranges[c]:
                    self.world_colored[y][x] = ('.', '#EEDD33')
                    self.world_normal[y][x] = ('.', self.integer_to_hex(self.normalize(self.world[y][x])))

                else:
                    self.world_colored[y][x] = ('~', '#4040FF')
                    self.world_normal[y][x] = ('~', self.integer_to_hex(self.normalize(self.world[y][x])))

    def output_terminal(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        for y in range(self.y):
            for x in range(self.x):
                yield (x, y, *world[y][x])    

if __name__ == "__main__":
    width, height = 80, 25
    setup(width, height)
    m = Map(width, height, .45, 7)
    m.generate()
    m.maxa()
    m.evaluate()
    while True:
        terminal.clear()
        for x, y, ch, col in list(m.output_terminal(True)):
            terminal.puts(x, y, '[c={}]{}[/c]'.format(col, ch))
        terminal.refresh()        
        key = terminal.read()
        if key_handle_exit(key):
            break