import os
import sys
import math
import color
import random
from bearlibterminal import terminal
from PIL import Image, ImageDraw

''' map functions '''
def steps_2_horizontal(inclusive=False):
    steps = set()
    for i in range(-1, 2, 1 if inclusive else 2):
        steps.add((i, 0))
    return steps

def steps_2_vertical(inclusive=False):
    steps = set()
    for i in range(-1, 2, 1 if inclusive else 2):
        steps.add((0, j))
    return steps

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

def steps_8_way(inclusive=False):
    steps = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i, j) != (0, 0):
                steps.add((i, j))
    if inclusive:
        steps.add((0, 0))
    return steps

def setup(x, y):
    terminal.open()
    terminal.set(f'window: size={x}x{y}, cellsize=8x8')
    terminal.refresh()

def key_handle_exit(key):
    if key in (terminal.TK_Q, terminal.TK_ESCAPE, terminal.TK_CLOSE):
        return True

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
            n = DrunkardsPeaks(m.width, m.height, .45, 15)  
            n.generate()
            m += n
            m.normalize()
            m.evaluate()

        elif key == terminal.TK_S:
            m.smooth()
            m.normalize()
            m.evaluate()

        elif key == terminal.TK_F:
            output_flag = not output_flag

class Map:
    def __init__(self, width, height, seed=None):
        self.width, self.height = width, height
        self.max, self.min = 0, 0
        self.seed = seed if seed else random.randint(0, 99999)
        random.seed(self.seed)

    def  __iadd__(self, other):
        if (self.width, self.height) != (other.width, other.height):
            raise ValueError('World Input has different dimensions')
        for y in range(self.height):
            for x in range(self.width):
                self.world[y][x] += other.world[y][x]
        self.normalize()
        return self

    def __imul__(self, other):
        # print(self.world[self.height//2][self.width//2], other.world[self.height//2][self.width//2])
        # print(self.max, other.max)
        if (self.width, self.height) != (other.width, other.height):
            raise ValueError('World Input has different dimensions')
        for y in range(self.height):
            for x in range(self.width):
                self.world[y][x] += other.world[y][x]
                self.world[y][x] /= 2
        self.normalize()
        return self      

    def base_single_flat(self):
        return [0 for _ in range(self.width)]

    def base_double_flat(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def base_single_float(self):
        return [random.random() * 2 - 1 for _ in range(self.width)]

    def base_double_float(self):
        return [[random.random() * 2 - 1 for _ in range(self.width)] for _ in range(self.height)]

    def percentage(self, value, percent):
        return value * percent

    def check_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height
        # x_lb = self.percentage(self.width, .1)
        # x_hb = self.percentage(self.width, .9)
        # y_lb = self.percentage(self.height, .1)
        # y_hb = self.percentage(self.height, .9)
        # return x_lb <= x < x_hb and y_lb <= y < y_hb

    def random_point(self):
        x_lb = self.percentage(self.width, .1)
        x_hb = self.percentage(self.width, .9)
        y_lb = self.percentage(self.height, .1)
        y_hb = self.percentage(self.height, .9)
        return random.randint(int(x_lb), int(x_hb)) , random.randint(int(y_lb), int(y_hb))
        # return random.randint(0, self.width - 1), random.randint(0, self.height - 1)

    def neighbors(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in steps_8_way(inclusive)]    

    def neighbors_lateral(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in steps_4_lateral()]    

    def neighbors_diagonal(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in steps_4_diagonal()]    

    def neighbors_horizontal(self, x, inclusive=False):
        return [x + step[0] for step in steps_2_horizontal(inclusive=inclusive)]

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

    def minmax_single(self):
        height = set()
        for x in range(self.width):
            if self.world[x] not in height:
                height.add(self.world[x])
        heights = sorted(height, reverse=True)
        self.max = heights[0]
        self.min = heights[-1]

    def smooth(self):
        world = self.base_double_flat()
        for y in range(self.height):
            for x in range(self.width):
                num, value = 0, 0
                for xx, yy in self.neighbors(x, y, inclusive=True):
                    try:
                        if (xx, yy) == (x, y):
                            value += self.world[yy][xx] * 2
                        else:
                            value += self.world[yy][xx]
                        num += 1
                    except IndexError:
                        pass
                world[y][x] = value / num

        # for y in range(self.height):
        #     for x in range(self.width):        
        #         self.world[y][x] *= world[y][x]      
        #         self.clamp(self.world[y][x])

        self.world = world
        # assert self.world == world

    def smooth_single(self, x1=None, x2=None):
        start, end = x1 if x1 else 0, x2 if x2 else len(self.world)
        world = self.base_single_flat()
        for x in range(start, end):
            num, value = 0, 0
            for xx in self.neighbors_horizontal(x, inclusive=True):
                try:
                    value += self.world[xx]
                    num += 1
                except IndexError:
                    pass

            world[x] = value / num
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

    def clamp(self, value):
        return max(0, min(value, 1))

    def integer_to_hex(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return '#' + value * 3

    def integer_to_red(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return '#' + value + '0000'

    def integer_to_green(self, value):
        value = self.pad(hex(int(value * 250)).split('x')[1])
        return '#' + '00' + value + '00'

    def integer_to_blue(self, value):
        value = self.pad(hex(int((1 - value) * 250)).split('x')[1])
        return '#' + '0000' + value

    def integer_to_yellow(self, value):
        # print(value)
        value = (1 - value) # .85
        r = self.pad(hex(int(value * .5 * 250)).split('x')[1])
        g = self.pad(hex(int(value * .8 * 250)).split('x')[1])
        b = self.pad(hex(int(value * .3 * 250)).split('x')[1])
        return '#' + r + g + b
        
    def split_range(self, number=25):
        return sorted([(self.max * i) / number for i in range(number)], reverse=True)

    def evaluate(self):
        self.maxmin()
        for y in range(self.height):
            for x in range(self.width):
                if .4 <= self.world[y][x]:
                    value = ('^', self.integer_to_hex(self.world[y][x]))
                    self.world_colored[y][x] = value
                    self.world_normal[y][x] = value

                elif .3 <= self.world[y][x] < .4:
                    self.world_colored[y][x] = ('"', self.integer_to_green(self.world[y][x]))
                    self.world_normal[y][x] = ('"', self.integer_to_hex(self.world[y][x]))

                elif 0.15 <= self.world[y][x] < .3:
                    self.world_colored[y][x] = (',', self.integer_to_green(self.world[y][x]))
                    self.world_normal[y][x] = (',', self.integer_to_hex(self.world[y][x]))

                elif 0.05 <= self.world[y][x] < .15:
                    self.world_colored[y][x] = ('.', self.integer_to_yellow(self.world[y][x]))
                    self.world_normal[y][x] = ('.', self.integer_to_hex(self.world[y][x]))

                else:
                    self.world_colored[y][x] = ('~', self.integer_to_blue(self.world[y][x]))
                    self.world_normal[y][x] = ('~', self.integer_to_hex(self.world[y][x]))

    def output_terminal(self, colored=False):
        world = self.world_colored if colored else self.world_normal
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y, *world[y][x])

    def output_image(self, colored=False, img_id=None):
        if not os.path.isdir('pics'):
            print('pics folder does not exist -- Creating "./logs"')
            os.makedirs('pics')

        world = self.world_colored if colored else self.world_normal
        img = Image.new('RGB', (self.width * 8, self.height * 8))
        ids = ImageDraw.Draw(img)
        for y in range(self.height):
            for x in range(self.width):
                ids.rectangle(
                    [x * 8, y * 8, x * 8 + 8, y * 8 + 8], world[y][x][1])
        img_name = (img_id + '_' if img_id else '') + self.__class__.__name__ + '.png'
        print(img_name)
        img.save('pics/' + img_name)        

class MPD(Map):
    def __init__(self, width, height, noise, seed=None):
        super().__init__(width=width, height=height, seed=seed)
        self.noise = noise
        self.world = self.base_single_float()

    def subdivide(self, x1, x2, delta):
        if x1 + 1 == x2:
            return

        x3 = (x1 + x2) // 2
        dy = (random.random() * 2 - 1) * delta

        # midpoint
        self.world[x3] = (self.world[x1] + self.world[x2] + self.world[x3]) / 3 + dy

        self.subdivide(x1, x3, delta * self.noise)
        self.subdivide(x3, x2, delta * self.noise)

    def serialdivide(self, x, end, delta):
        if x == end:
            return

        dy = (random.random() * 2 - 1) * delta
        self.world[x + 1] = (self.world[x] + self.world[x + 2]) / 2 + dy

        self.subdivide(x + 1, end, delta * self.noise)

class Drunkards(Map):
    def __init__(self, width, height, limit, seed=None):
        super().__init__(width=width, height=height, seed=seed)
        self.limit = int(height * width * limit)

        self.world = self.base_double_flat()
        self.world_normal = self.base_double_flat()
        self.world_colored = self.base_double_flat()

        self.generate()

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
        # print(width, height, limit, peaks)
        self.world = self.base_double_flat()
        self.world_normal = self.base_double_flat()
        self.world_colored = self.base_double_flat()

        x_lb = self.percentage(self.width, .3)
        x_hb = self.percentage(self.width, .7)
        y_lb = self.percentage(self.height, .3)
        y_hb = self.percentage(self.height, .7)

        self.peaks = [(
            random.randint(int(x_lb), int(x_hb)) , 
            random.randint(int(y_lb), int(y_hb))) 
            for _ in range(peaks)]
        # self.peaks = [(
        #     random.randint(width // 2 - width // 4, width // 2 + width // 4), 
        #     random.randint(height // 2 - height // 3, height // 2 + height // 3)) 
        #         for _ in range(peaks)]

        for px, py in self.peaks:
            self.world[py][px] = 5

        self.generate()

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

def test_midpoint_single(width, height, noise=.7, seed=None):
    line = MPD(width=width, height=height, noise=noise, seed=seed)
    line.subdivide(0, width-1, 50)
    # line.serialdivide(0, width - 1, 50)
    line.minmax_single()

    total = line.max - line.min
    print(total, line.max, line.min)
    while True:
        terminal.clear()
        for i in range(width):
            terminal.puts(i, int(round((line.world[i] - line.min)) / (total) * height), '.')
        terminal.refresh()
        key = terminal.read()
        if key_handle_exit(key):
            terminal.close()
            break
        elif key == terminal.TK_S:
            line.smooth_single()

def test_drunkards(width, height, noise, seed=None):
    m = Drunkards(width, height, noise, seed)
    m.normalize()
    m.evaluate()
    term_loop(m)

def test_drunkards_peaks(width, height, noise, peaks, seed=None):
    m = DrunkardsPeaks(width, height, noise, peaks)
    m.normalize()
    m.evaluate()
    term_loop(m)

def test_combination(width, height, maps):
    m = DrunkardsPeaks(width, height, .45, 13)  

    m.generate()
    m.evaluate()

    term_loop(m)

def test_combination_image(width, height, maps):
    m = DrunkardsPeaks(width, height, .35, 10)
    # m = Drunkards(width, height, .45)
    m.evaluate()  
    m.output_image(colored=True, img_id='0')
    # n = m
    # n.smooth()
    # n.evaluate()  
    # n.output_image(colored=True, img_id='1')
    for i in range(maps - 1):
        # if random.randint(0, 1):
        #     print('peak')
        # n = DrunkardsPeaks(width, height, .2, 2)
        # else:
        #     print('drunk')
        n = Drunkards(width, height, .2)
        n.evaluate()
        n.output_image(colored=True, img_id=str((i + 1) * 2))
        m *= n
        m.evaluate()
        m.output_image(colored=True, img_id=str((i + 1) * 2 + 1))
    m.output_image(colored=False, img_id=str((i + 1) * 2 + 1) + 'c')

    for j in range(3):
        m.smooth()

    m.evaluate()
    m.output_image(colored=True, img_id=str((i + 1) * 2 + 2))
    m.output_image(colored=False,img_id=str((i + 1) * 2 + 2) + 'c')
    print(m.min)

if __name__ == "__main__":
    width, height = 480, 270

    # width, height = 80, 25
    # setup(width, height)

    # seed = random.randint(0, 99999)
    # print(seed)

    seed = None
    # test_drunkards(width, height, .45)
    # test_drunkards_peaks(width, height, .45, 13, seed)
    # test_combination(width, height, 3)
    # test_midpoint_single(width, height, .7)

    test_combination_image(width, height, 2)