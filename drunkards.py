import math
import color
import random
import randomfill
from mpd_one_dim import setup, key_handle_exit
from bearlibterminal import terminal
from PIL import Image, ImageDraw

''' map functions '''
def steps_4_diagonal():
    steps = set()
    for i in range(-1, 2, 2):
        for j in range(-1, 2, 2):
            steps.add((i, j))
    return steps

def steps_4_lateral():
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

def term_loop(m):
    output_flag = False
    while True:
        # console.clear()
        terminal.clear()
        for x, y, ch, col in list(m.output_terminal(output_flag)):
            terminal.puts(x, y, '[c={}]{}[/c]'.format(col, ch))
        terminal.refresh()

        key = terminal.read()
        if key_handle_exit(key):
            break

        elif key == terminal.TK_A:
            print('aa')
            n = DrunkardsPeaks(200, 60, .45, 13)  
            n.generate()
            m += n

        elif key == terminal.TK_S:
            m.smooth()
            m.normalize()
            m.evaluate()

        elif key == terminal.TK_F:
            output_flag = not output_flag

class Map:
    def __init__(self, width, height, seed=None):
        self.width, self.height = width, height

        self.world = self.create_base()
        self.world_normal = self.create_base()
        self.world_colored = self.create_base()

        self.seed = seed if seed else random.randint(0, 99999)
        random.seed(self.seed)

    def  __iadd__(self, other):
        if (self.width, self.height) != (other.width, other.height):
            raise ValueError('World Input has different dimensions')
        for y in range(self.height):
            for x in range(self.width):
                self.world[y][x] += other.world[y][x]
        return self

    def __imul__(self, other):
        # print(self.world[self.height//2][self.width//2], other.world[self.height//2][self.width//2])
        # print(self.max, other.max)
        if (self.width, self.height) != (other.width, other.height):
            raise ValueError('World Input has different dimensions')
        for y in range(self.height):
            for x in range(self.width):
                self.world[y][x] *= other.world[y][x]
        return self       

    def create_base(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def check_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def random_point(self):
        return random.randint(0, self.width - 1), random.randint(0, self.height - 1)

    def neighbors_inclusive(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_9_way()]    

    def neighbors_exclusive(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_8_way()]    

    def neighbors_lateral(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_4_lateral()]    

    def neighbors_diagonal(self, x, y):
        return [(x + step[0], y + step[1]) for step in steps_4_diagonal()]    

    def generate(self):
        raise NotImplementedError('Use child map class instead')

    def maxmin(self):
        height = set()
        for y in range(self.height):
            for x in range(self.width):
                if self.world[y][x] not in height:
                    height.add(self.world[y][x])

        heights = sorted(height, reverse=True)
        self.max = heights[0]
        self.min = heights[-1]

    def smooth(self):
        world = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                num = 0
                value = 0
                for xx, yy in self.neighbors_inclusive(x, y):
                    try:
                        value += self.world[yy][xx]
                        num += 1
                    except IndexError:
                        pass
                world[y][x] = value / num
        self.world = world

    def normalize(self, norm=1):
        self.maxmin()
        world = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                world[y][x] = (self.world[y][x] / self.max) * norm
        self.world = world
        self.maxmin()

    def pad(self, value):
        if len(value) < 2:
            return "0" + value
        return value

    def integer_to_hex(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return '#' + value * 3

    def integer_to_red(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return' #' + value + '0000'

    def integer_to_green(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return' #' + '00' + value + '00'

    def integer_to_blue(self, value):
        value = self.pad(hex(int((1 - value) * 250)).split('x')[1])
        return' #' + '0000' + value

    def split_range(self, number=25):
        return sorted([(self.max * i) / number for i in range(number)], reverse=True)

    def evaluate(self):
        self.maxmin()
        for y in range(self.height):
            for x in range(self.width):
                if .6 <= self.world[y][x]:
                    value = ('^', self.integer_to_hex(self.world[y][x]))
                    self.world_colored[y][x] = value
                    self.world_normal[y][x] = value

                elif .3 <= self.world[y][x] < .6:
                    self.world_colored[y][x] = ('"', self.integer_to_green(self.world[y][x]))
                    self.world_normal[y][x] = ('"', self.integer_to_hex(self.world[y][x]))

                elif .05 <= self.world[y][x] < .3:
                    self.world_colored[y][x] = ('.', self.integer_to_green(self.world[y][x]))
                    self.world_normal[y][x] = ('.', self.integer_to_hex(self.world[y][x]))

                else:
                    self.world_colored[y][x] = ('~', self.integer_to_blue(self.world[y][x]))
                    self.world_normal[y][x] = ('~', self.integer_to_hex(self.world[y][x]))

    def output_terminal(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, *world[y][x])

    def output_image(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        img = Image.new('RGB', (self.width * 8, self.height * 8))
        ids = ImageDraw.Draw(img)
        for y in range(self.height):
            for x in range(self.width):
                ids.rectangle(
                    [x * 8, y * 8, x * 8 + 8, y * 8 + 8], world[y][x][1])
        img.save(self.__class__.__name__ + '.png')        

class Drunkards(Map):
    def __init__(self, width, height, limit, seed=None):
        super().__init__(width, height, seed)
        self.limit = int(height * width * limit)

    def generate(self): 
        """ Returns map filled with drunkards height algo """
        self.spaces = set()
        ry, rx = self.random_point()

        while len(self.spaces) <= self.limit:
            step = random.choice(list(steps_4_lateral()))
            # if at somepoint we are at the edge of the map and choose
            # a point outside of the map bounds we choose a random point
            # from the map to start the process again
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        self.normalize()

class DrunkardsPeaks(Map):
    def __init__(self, width, height, limit, peaks, seed=None):
        """Drunkards algorithm with peaks"""
        super().__init__(width, height, seed)
        self.limit = int(width * height * limit)
        self.peaks = [(
            random.randint(width // 2 - width // 4, width // 2 + width // 4), 
            random.randint(height // 2 - height // 3, height // 2 + height // 3)) 
                for _ in range(peaks)]

    def random_point(self):
        # return randint(0, self.x -1), randint(0, self.y - 1)
        return self.peaks[random.randint(0, len(self.peaks) - 1)]

    def generate(self):
        self.spaces = set()
        rx, ry = self.random_point()
        while len(self.spaces) <= self.limit:
            step = random.choice(list(steps_4_lateral()))
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        self.normalize()

def test_drunkards():
    width, height = 160, 50
    setup(width, height)

    m = Drunkards(width, height, .45)
    m.generate()
    # m.smooth()
    # m.smooth()
    m.normalize()
    m.evaluate()

    term_loop(m)

def test_drunkards_peaks():
    width, height = 160, 50
    setup(width, height)

    m = DrunkardsPeaks(width, height, .3, 7)
    m.generate()
    m.normalize()
    m.evaluate()

    term_loop(m)

def test_combination():
    width, height = 200, 60
    setup(width, height)
    
    m = DrunkardsPeaks(width, height, .45, 13)  

    m.generate()
    m.evaluate()

    term_loop(m)

if __name__ == "__main__":
    # test_drunkards()
    # test_drunkards_peaks()
    test_combination()