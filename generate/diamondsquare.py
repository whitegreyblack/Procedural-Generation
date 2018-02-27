import math
import random
from color import Color
from copy import deepcopy
from pprint import pprint
from PIL import Image, ImageDraw
from header import line, randfloat
from collections import namedtuple
from combinations import Sequences

'''DSW map manipulation functions should be changed into self returning methods
which should allow for function chaining, giving a way for the user to easily 
follow the methods used in producing the desired end results of the generated 
map. Any data manipulation should work on DSW.map and return dsw object.
'''

Point = namedtuple("Point", "x y")
Box = namedtuple("Box", "x1 y1 x2 y2")

class DSW:
    photos = 0
    LAND = "#008855"
    TREE = "#004422"
    WATER = "#005577"
    MOUNT = "#BBBBBB" 

    def __init__(self, power, noise=.5, delta=.8, seed=None, generate=True):
        '''Sets the map size and creates the 2d map to hold float values. Then
        runs the diamond-square algorithm to populate the array. Finally calls
        normalize to set the values in the map from [0-1] inclusive.
        '''
        size = 2 ** power + 1
        self.colorized = False
        self.width, self.height = size, size
    
        self.seed = seed
        if not seed:
            self.seed = random.randint(0, 999999)
        random.seed(self.seed)

        # initialize to zero
        self.map = [[0.0 for j in range(size)] for i in range(size)]
        # self.hex = [[0.0 for j in range(size)] for i in range(size)]
        # self.clr = [[0.0 for j in range(size)] for i in range(size)]

        if generate:
            self.run(noise, delta)
            self.normalize()

    def at(self, x, y): 
        return self.map[y][x]

    def put(self, x, y, v): 
        self.map[y][x] = v

    def run(self, noise, delta):
        '''Initialization of variables used in the diamon square recursive
        method. Sets the box size to the map dimensions and the 4 corners of
        the map to a random float value. Can also initialize other variables
        if the user wants to change the starting state before running dsa.
        '''
        
        box = Box(0, 0, self.width - 1, self.height - 1)
        
        # initialize corners
        self.put(box.x1, box.y1, randfloat())
        self.put(box.x1, box.y2, randfloat())
        self.put(box.x2, box.y1, randfloat())
        self.put(box.x2, box.y2, randfloat())

        # start recursive function
        self.diamondsquare(noise, delta, box)

    def diamondsquare(self, noise, delta, box):
        '''Recursive function which create randomly controlled values at every
        iteration onto the spaces within the parameter box in a diamond and 
        then square form. Noise is halved at each step of the iteration.
        '''
        def diamond(x, y, p1, p2, p3):
            self.put(x, y, ((p1 + p2 + p3) / 3) + randfloat() * random.uniform(-noise, noise))

        hx, hy = (box.x2 - box.x1) // 2, (box.y2 - box.y1) // 2
        # print(hx, hy)
        # exit()

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

        # sets the middle point (point 5) of the square using points 1, 3, 7, 9
        self.put(p5.x, p5.y, ((p1 + p3 + p7 + p9) / 4) + randfloat() * random.uniform(-noise, noise))
        
        p5 = self.at(p5.x, p5.y)
        
        x8, y8 = box.x1 + hx, box.y1
        x4, y4 = box.x1, box.y1 + hy
        x6, y6 = box.x2, box.y1 + hy
        x2, y2 = box.x1 + hx, box.y2	

        # TODO :- currently flawed  
        diamond(x8, y8, p5, p7, p9)
        diamond(x4, y4, p1, p5, p7)
        diamond(x6, y6, p3, p5, p9)
        diamond(x2, y2, p1, p3, p5)
        # self.put(x2, y2, ((p1 + p3 + p5) / 3) + random.uniform(-noise, noise))
        # self.put(x8, y8, ((p1 + p5 + p7) / 3) + random.uniform(-noise, noise))
        # self.put(x6, y6, ((p3 + p5 + p9) / 3) + random.uniform(-noise, noise))
        # self.put(x4, y4, ((p5 + p7 + p9) / 3) + random.uniform(-noise, noise))

        noise = noise / (2 ** -.15)

        if box.x2 - box.x1 > 2 or box.y2 - box.y1 > 2:
            # quadrant 4
            self.diamondsquare(noise, delta, Box(box.x1, 
                                                 box.y1, 
                                                 box.x1 + hx, 
                                                 box.y1 + hy))
            
            # quadrant 13
            self.diamondsquare(noise, delta, Box(box.x1 + hx, 
                                                 box.y1, 
                                                 box.x2, 
                                                 box.y1 + hy))
            
            # quadrant 1
            self.diamondsquare(noise, delta, Box(box.x1, 
                                                 box.y1 + hy,
                                                 box.x1 + hx, 
                                                 box.y2))

            # quadrant 2
            self.diamondsquare(noise, delta, Box(box.x1 + hx, 
                                                 box.y1 + hy, 
                                                 box.x2, 
                                                 box.y2))
        
    def prettify(self, array):
        for row in array:
            print(" ".join(map(lambda x: f"{x:6.2f}", row)))
    
    def copy(self):
        return deepcopy(self)
    
    def normalize(self):
        self.zvalues = [cell for row in self.map for cell in row]
        nmin = min(self.zvalues)
        nmax = max(self.zvalues)

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.map[y][x] = (cell - nmin) / (nmax - nmin)
                self.zvalues[self.width * y + x] = self.map[y][x]
        # self.zvalues = [cell for row in self.map for cell in row]
        # self.values = sort_values(self.values)
        # self.prettify(self.values)
        return self

    def crosscheck(self, other):
        if self.colorized or other.colorized:
            return False
        return True

    def additive(self, other):
        if not self.crosscheck(other):
            raise ValueError("Cannot multiple non-float maps together")
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.map[y][x] += other.map[y][x]
        self.normalize()
        return self

    def multiply(self, other):
        if not self.crosscheck(other):
            raise ValueError("Cannot multiple non-float maps together")
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                self.map[y][x] *= other.map[y][x]
        self.normalize()
        return self

    def replace(self, other):
        if not self.crosscheck(other):
            raise ValueError("Cannot multiple non-float maps together")
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if other.map[y][x] > self.map[y][x]:
                    self.map[y][x] = other.map[y][x]
        self.normalize()
        return self

    def colorize(self, color=False):
        def sort_values(values):
            import numpy
            hist, bin_edges = numpy.histogram(self.map, bins=20)
            valuepairs = [z for z in zip(list(hist), bin_edges)]
            return valuepairs
            # return sorted(valuepairs, reverse=True)

        def float_to_clr(x):
            '''Returns chosen hex formatted color codes representing specific
            areas on the map.
            '''
            if x >= self.values[16][1]:
                return self.MOUNT
            
            # elif self.values[self.forests] <= x < self.values[self.mountains]:
            #     return "#000000"
            elif x >= self.values[13][1]:
                return self.TREE
            elif x >= self.values[10][1]:
                return self.LAND

            else:
                return self.WATER

        def float_to_hex(x):
            '''Returns chosen hex formatted b/w codes representing float value
            as a hex color code
            '''
            value = hex(round(x * 250)).split('x')[1]
            if len(value) < 2:
                value = '0' + value
            return '#' + value * 3

        if self.colorized:
            raise ValueError("Map has already been converted to a color map")
            
        self.colorized = True

        if color:
            self.values = sort_values(self.zvalues)

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                if color:
                    self.map[y][x] = float_to_clr(cell)
                else:
                    self.map[y][x] = float_to_hex(cell)
        return self

    def snapshot(self, color=False):
        array = self.map
        if isinstance(array[0][0], float):
            array = deepcopy(self).colorize(color=color).map

        img = Image.new('RGB', (self.width, self.height))
        ids = ImageDraw.Draw(img)

        for y, row in enumerate(array):
            for x, cell in enumerate(row):
                # pass
                ids.point([x, y, x, y], cell)
                # ids.rectangle([x, y, x, y], cell)
        
        img.save(f"../pics/dsw_{DSW.photos}_{'rgb' if color else 'bw'}.png")
        DSW.photos += 1

    def smooth(self, times=1):
        if not isinstance(self.map[0][0], float):
            raise ValueError('smoothing cannot be applied on maps of non float types')

        for _ in range(times):
            smooth = deepcopy(self.map)
            for j, row in enumerate(smooth):
                for i, cell in enumerate(row):
                    val = []
                    for jj in range(-1, 2):
                        for ii in range(-1, 2):
                            (ii, jj)
                            height = 0.0
                            try:
                                height = self.map[j+jj][i+ii]
                            except IndexError:
                                height = self.map[j][i]
                            val.append(height)
                    smooth[j][i] = sum(val) / len(val)
            self.map = smooth
        return self

    def sort_array_max(self):
        '''Sorts the 2d array map into a 1D array of values descending'''
        def distance(i, j):
            '''Heuristic function used to sort keyvalues in sorted()'''
            x = (self.width // 2) - i
            y = (self.height // 2) - j
            return math.sqrt((x * x) + (y * y))

        maxes = sorted([(x, i, j) for j, y in enumerate(self.map) 
                            for i, x in enumerate(y)
                                if x > self.values[self.grassland]], 
                        reverse=True,
                        key=lambda x: (x[0], distance(x[1], x[2])))

        print(maxes[0], maxes[1], maxes[2])
        
        for x, y in line((maxes[0][1:]), maxes[random.randint(1, len(maxes) - 2)][1:]):
            self.clr[y][x] = "#4433AA"

        for x, y in line((maxes[0][1:]), maxes[random.randint(1, len(maxes) - 2)][1:]):
            self.clr[y][x] = "#4433AA"

        # for x, y in line((maxes[1][1:]), maxes[2][1:]):
        #     self.clr[y][x] = "#4433AA"

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
                    # print('removing', i, j)
                    new_map[j][i] = self.WATER if x == self.LAND else self.LAND

        self.clr = deepcopy(new_map)
        return self

if __name__ == "__main__":
    seed = random.randint(0, 99999)
    print(seed)
    random.seed(seed)
    size = 6
    # dsw = DSW(size, noise=.72, delta=.8)
    # dsw.prettify()
    # term_print(dsw.hex, 6)
    # norm_print(dsw.hex, size, pid='0')

    # question: at this point should the DSW.map be initizalized or run?
    # verdict: it should be ran on object instantiation
    #
    # question: at this point should the DSW.map be normalized?
    # verdict: yes it should be normalized for easier user usage
    m = DSW(size, noise=.25, delta=.75).smooth(2).snapshot()

    # bins = 100
    # hist, bin_edges = numpy.histogram(dsw.map, bins=bins)
    # print(hist, bin_edges)
    # plt.hist([x for y in dsw.map for x in y], bins=bins)
    # plt.show()
    # print(hist)

    # norm_print(dsw.hex, size, pid='1n')
    # color_print(dsw.clr, size, pid='1c')

    # heat = DSW(size, noise=.55, delta=.65)