import os
import sys
import math
import random
from PIL import Image, ImageDraw
from random import random, randint
from bearlibterminal import terminal
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
import generate.color

def lpath(b1, b2):
    # x1, y1 = center(b1)
    # x2, y2 = center(b2)
    x1, y1 = b1
    x2, y2 = b2

    # check if xs are on the same axis -- returns a vertical line
    if x1 == x2 or y1 == y2:
        return line((x1, y1), (x2, y2))

    # # check if points are within x bounds of each other == returns the midpoint vertical line
    # elif b2.x1 <= x1 < b2.x2 and b1.x1 <= x2 < b1.x2:
    #     x = (x1+x2)//2
    #     return line((x, y1), (x, y2))

    # # check if points are within y bounds of each other -- returns the midpoint horizontal line
    # elif b2.y1 <= y1 < b2.x2 and b1.y1 <= y2 < b2.y2:
    #     y = (y1+y2)//2
    #     return line((x1, y), (x2, y))

    else:
        # we check the slope value between two boxes to plan the path
        slope = abs((max(y1, y2) - min(y1, y2))/((max(x1, x2) - min(x1, x2)))) <= 1.0
    
        # low slope -- go horizontal
        if slope:
            # width is short enough - make else zpath
            return line((x1, y1), (x1, y2)) \
                + line((x1, y2), (x2, y2))

        # high slope -- go vertical
        else:
            return line((x1, y1), (x2, y1)) + line((x2, y1), (x2, y2))

def line(start, end):
    """Bresenham's Line Algo -- returns list of tuples from start and end"""

    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def constructor(width, height=None, depth=None, value=None, args=None):
    '''Returns either a 1D, 2D or 3D array depending on height parameter
    and assigns each value in the array a value passed in as a parameter.
    The value can also take in arguments passed in as a parameter which 
    it uses to create the final value in the array
    '''
    def determine():
        '''Helper function for constructor that allows constructor to 
        calculate the final value that will be returned and placed in 
        the array
        '''
        ret = 0
        if callable(value):
            if callable(args):
                ret = value(args())
            elif args:
                ret = value(*args)
            else:
                ret = value()
        elif value:
            ret = value
        return ret

    if not width:
        raise ValueError('Width must be specified')

    if not height and depth:
        # cannot have height but have depth -- just switch it in that case
        height, depth = depth, height

    array = None
    dimensions = sum(map(lambda x: 1 if x else 0, (width, height, depth)))
    
    for _ in range(dimensions):
        if not array:
            array = [determine() for _ in range(width)]
        elif isinstance(array[0], int) or isinstance(array[0], float):
            array = [array for _ in range(height)]
        else:
            array = [array for _ in range(depth)]
    return array

def setup(x, y, cx=8, cy=8):
    terminal.open()
    terminal.set(f'window: size={x}x{y}, cellsize={cx}x{cy}')
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
        return [(x + step[0], y + step[1]) for step in Combinations.combinations(Combinations.ALL, inclusive=inclusive)]    

    def neighbors_lateral(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in Combinations.combinations(Combinations.LATERAL, inclusive=inclusive)]    

    def neighbors_diagonal(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in Combinations.combinations(Combinations.DIAGONAL, inclusive=inclusive)]    

    def neighbors_horizontal(self, x, inclusive=False):
        return [x + step[0] for step in Combinations.combinations(Combinations.HORIZONTAL, inclusive=inclusive)]

    def generate(self):
        self.world_colored = None
        self.world_normal = None
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
                            value += self.world[yy][xx] * 1.5
                        else:
                            value += self.world[yy][xx] * .5
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

def convert_tile_map(tilemap):
    pass

if __name__ == "__main__":
    width, height = 240, 160
    print(__file__)