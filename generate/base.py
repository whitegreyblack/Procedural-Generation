import os
import sys
import math
import random
from PIL import Image, ImageDraw
from bearlibterminal import terminal
import color
from combinations import Sequences

class Map:
    '''Map class only initializes properties used across all map classes:
        width, height, and seed
    The class also implements map addition, multiplication and other similar
    functions used in multiple map combinations and blending
    ''' 
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
        return (random.randint(int(x_lb), int(x_hb)), 
                random.randint(int(y_lb), int(y_hb)))
        # return random.randint(0, self.width - 1), random.randint(0, self.height - 1)

    def neighbors(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) 
                for step in Combinations.combinations(
                    combination=Combinations.ALL, 
                    inclusive=inclusive)]    

    def neighbors_lateral(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) 
                for step in Combinations.combinations(
                    combination=Combinations.LATERAL, 
                    inclusive=inclusive)]    

    def neighbors_diagonal(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) 
                for step in Combinations.combinations(
                    combination=Combinations.DIAGONAL, 
                    inclusive=inclusive)]    

    def neighbors_horizontal(self, x, inclusive=False):
        return [x + step[0] 
                for step in Combinations.combinations(
                    combination=Combinations.HORIZONTAL, 
                    inclusive=inclusive)]

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
        self.max, self.min = heights[0], heights[-1]

    def smooth(self):
        world = self.base_double_flat()

        for y in range(self.height):
            for x in range(self.width):
                num, value = 0, 0

                for xx, yy in self.neighbors(x, y, inclusive=True):
                    try:
                        if (xx, yy) == (x, y):
                            value += self.world[yy][xx]

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
        # value = (1 - value) # .85
        # r = self.pad(hex(int(value * .5 * 250)).split('x')[1])
        # g = self.pad(hex(int(value * .8 * 250)).split('x')[1])
        # b = self.pad(hex(int(value * .3 * 250)).split('x')[1])
        return '#deef88'
        
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

if __name__ == "__main__":
    print(__file__)
    base = Map(width=100, height=100)