import os
import sys
import math
import color
import random
from color import Color
from bearlibterminal import terminal
from PIL import Image, ImageDraw
# MAP FUNCTIONS\
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

class Combinations:
    HORIZONTAL, VERTICAL, DIAGONAL, LATERAL, ALL = range(5)

    @staticmethod
    def types():
        return (Combinations.HORIZONTAL,
            Combinations.VERTICAL,
            Combinations.DIAGONAL,
            Combinations.LATERAL,
            Combinations.ALL)

    @staticmethod
    def combinations(combination, inclusive=False):
        if combination not in Combinations.types():
            raise ValueError("Invalid Combination")
        steps = set()
        if combination == Combinations.HORIZONTAL:
            for i in range(-1, 2, 2):
                steps.add((i, 0))
        elif combination == Combinations.VERTICAL:
            for j in range(-1, 2, 2):
                steps.add((0, j))
        elif combination == Combinations.DIAGONAL:
            for i in range(-1, 2, 2):
                for j in range(-1, 2, 2):
                    steps.add((i, j))
        elif combination == Combinations.LATERAL:
            for i in range(-1, 2, 2):
                steps.add((0, i))
                steps.add((i, 0))
        elif combination == Combinations.ALL:
            for j in range(-1, 2):
                for i in range(-1, 2):
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
        return [(x + step[0], y + step[1]) for step in Combinations.combinations(Combinations.ALL, inclusive=inclusive)]    

    def neighbors_lateral(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in Combinations.combinations(Combinations.LATERAL, inclusive=inclusive)]    

    def neighbors_diagonal(self, x, y, inclusive=False):
        return [(x + step[0], y + step[1]) for step in combinations.combinations(Combinations.DIAGONAL, inclusive=inclusive)]    

    def neighbors_horizontal(self, x, inclusive=False):
        return [x + step[0] for step in combinations.combinations(Combinations.HORIZONTAL, inclusive=inclusive)]

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
            step = random.choice(list(Combinations.combinations(Combinations.LATERAL, inclusive=False)))
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
            step = random.choice(list(Combinations.combinations(Combinations.LATERAL, inclusive=False)))
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        self.normalize()

class DrunkardsPeaksImproved(Map):
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
   
class Node:
    def __init__(self, node_id, x, y):
        self.id = node_id
        self.x, self.y = x, y
        self.neighbors = {}

    def __str__(self):
        return f"Node {self.id}: ({self.x}, {self.y})"

    def __repr__(self):
        return f"Node {self.id}: ({self.x}, {self.y})"

    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 + (other.y - self.y) ** 2)

    def closest(self):
        if self.neighbors:
            return min((self.neighbors[k], k) for k in self.neighbors)

    def vertices(self):
        return set((self.neighbors[k], min(self.id, k), max(self.id, k)) for k in self.neighbors)
            
class Room(Node):
    def __init__(self, node_id, x, y, width=8, height=5):
        super().__init__(node_id, x, y)
        self.width, self.height = width, height
        x1, x2, y1, y2 = self.x - width//2, self.x + width//2 + 1, self.y - height//2, self.y + height//2 + 1
        self.x1, self.x2, self.y1, self.y2 = x1, x2, y1, y2
        self.top_left = (x1, y1)
        self.top_right = (x1, y2)
        self.bot_left = (x2, y1)
        self.bot_right = (x2, y2)
        self.color = Color()

    @property
    def points(self):
        points = set()
        for j in range(self.y1, self.y2):
            for i in range(self.x1, self.x2):
                points.add((i, j))
        return points

    @property
    def walls(self):
        points = set()
        # get x axis
        for j in range(self.y1, self.y2):
            points.add((self.x1, j))
            points.add((self.x2 - 1, j))
        # get y axis
        for i in range(self.x1, self.x2):
            points.add((i, self.y1))
            points.add((i, self.y2 - 1))
        return points

    @property
    def floors(self):
        points = set()
        for j in range(self.y1 + 1, self.y2 - 1):
            for i in range(self.x1 + 1, self.x2 - 1):
                points.add((i, j))
        return points

    @property
    def corners(self):
        return {self.top_left, self.top_right, self.bot_left, self.bot_right}

    def random_point(self):
        return random.choice(list(self.points))

    def random_wall_point(self):
        return random.choice(list(self.walls))

    def random_floor_point(self):
        return random.choice(list(self.floors))

class MST():
    '''Takes in list/set of nodes amd returns a minimum spanning tree.'''
    def __init__(self, nodes=None, noise=.8):
        self.nodes = nodes if nodes else []

    def __repr__(self):
        return f"MST: nodes: {len(self.nodes)}\n  " + \
        "\n  ".join([f"{k}, {self.graph[k]}" for k in self.graph])

    def run(self):
        '''The algorithm follows minimum spanning tree however there are
        several conditions that will be checked during the iterations.

        1. If the nodes are too far apart, will not connect
        2. If graph is not completely connected, will return all groups
           in their own set.
        3. If more than one group, leads to multiple continents
        '''
        self.mst = set()
        pq = sorted(self.edges)
        print('PQ', pq)
        while pq:
            d, a, b = pq.pop(0)
            # if d >= 15:
            #     break
            # print(a, ':', self.vertices[a], ',', b, ':', self.vertices[b])
            if b not in self.vertices[a] and a not in self.vertices[b]:
                # print('adding', b, '->', a, ':', self.vertices[a])
                self.vertices[a].update(self.vertices[b])
                for c in self.vertices[a]:
                    self.vertices[c] = self.vertices[a]
                    # print('UPDATE', c, self.vertices[c])
                # print('adding', a, '->', b, ':', self.vertices[b])
                self.vertices[b].update(self.vertices[a])
                for c in self.vertices[b]:
                    self.vertices[c] = self.vertices[b]
                    # print('UPDATE', c, self.vertices[c])
                # print(a, ':', self.vertices[a], ',', b, ':', self.vertices[b])
                self.mst.add((a, b))
                if len(self.mst) == len(self.nodes) - 1:
                    break

        # more = int(len(pq) * .01)
        more = int(len(self.nodes) * .3)
        print(more)
        for i in range(min(more, len(pq))):
            d, a, b = pq.pop(0)
            self.mst.add((a, b))
            # if len(self.mst) == len(self.nodes) - 1:
            #     break
            # print()

    def calculate_distances(self):
        if not self.nodes:
            raise ValueError('No nodes in graph')
        for i in self.nodes:
            for j in self.nodes:
                if i != j:
                    i.neighbors[j.id] = i.distance(j)

        self.graph = {node: node.neighbors for node in self.nodes}
        # for k in self.graph:
        #     print(k, self.graph[k])

    def node_with_id(self, nid):
        node = None
        for n in self.nodes:
            if n.id == nid:
                node = n
        return node

    def add(self, node):
        self.nodes.append(node)

    def find_all_edges(self):
        self.edges = {v for node in self.nodes for v in node.vertices()}

    def find_all_vertices(self):
        self.vertices = {node.id: {node.id} for node in self.nodes}

    def output_terminal(self, line=line):
        vertices = set()
        for n in self.nodes:
            vertices.add((n.x, n.y))
            terminal.puts(n.x, n.y, f'[c=red]@[/c]')
        for a, b in self.mst:
            na = self.node_with_id(a)
            nb = self.node_with_id(b)
            for (x, y) in line((na.x, na.y), (nb.x, nb.y))[1:-1]:
                if (x, y) not in vertices:
                    terminal.puts(x, y, f'[c=white].[/c]')
        terminal.refresh()
        terminal.read()

    def output_post_processing(self, line=line):
        pass

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
