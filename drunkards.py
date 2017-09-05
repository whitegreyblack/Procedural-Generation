import random
import math
import color as c
import queue
from collections import namedtuple
from copy import deepcopy

GRN = "\x1b[0;32;40m"
END = "\x1b[0m"

seedNum = namedtuple("Seed", (['seed']))
tileLen = namedtuple("Tile", (["x", "y"]))
class Territory:
    def __init__(self, pos):
        self. pos = pos

class Kingdom:
    def __init__(self, capital):
        self.capital = capital
        self.land = (capital)
        self.pq = queue.PriorityQueue()

    def expand(self, land):
        self.land.append(land)

    def border(self, land):
        return land in self.land

    def neighbors(self):
        for i in self.land:
            for j in range(3):
                for k in range(3):
                    pass
class Map:
    """ Drunkards Algorithm with Height Map implementation """
    def __init__(self, x, y, cells, seed=None):
        self.x = x
        self.y = y
        self.world = [[0 for i in range(self.y)] for j in range(self.x)]
        self.mini = 0
        self.maxa = 0
        self.valid = []
        self.lim = x*y*cells
        self.clans = deepcopy(self.world)
        self.height = deepcopy(self.world)
        self.rainfall = deepcopy(self.world)
        self.kingdoms = []
        #self.kingdoms = [None for i in range(int(self.x*self.y/1000*1.5))]
        self.temperature = deepcopy(self.world)
        self.seed = random.randint(0,99999)
        print(seedNum(self.seed if not seed else seed))
        random.seed(seed if seed != None else self.seed)
        self.build()

    def checkbounds(self, tx, ty):
        if not 3 < tx < int(self.x-4):
            tx = self.x//2
        if not 3 < ty < int(self.y-4):
            ty = self.y//2
        return (tx, ty)

    def build(self):
        self.heightify()
        self.waterfy()
    
    def getNeighbors(self, land):
        x, y = land
        for i in self.kingdoms:
            pass
        
    # each functions should take in valid points and return split sets / kingdom
    #   input: (valid points)
    def circlefill(self): pass
    def spiralfill(self): pass
    def breadthfill(self): pass
    def closestfill(self): pass
    def randomfill(self): pass
    def chosenfill(self): pass
    def addClans(self):
        def getneighbors(x):
            xx, xy = x
            neighbors = []
            for i in range(-1,2):
                for j in range(-1,2):
                    if 0 <= xx+i < len(world) and 0 <= xy+j < len(world[i]):
                        if (xx+i, xy+j) != x and world[xx+i][xy+j] > 0:
                            neighbors.append((xx+i, xy+j))
            return neighbors
        def manhattan(x, y):
            xa, xb = x
            ya, yb = y
            return abs(xa-ya)+abs(xb-yb)
        def chebyshev(x, y):
            xa, xb = x
            ya, yb = y
            return int(1 * manhattan(x, y) + (math.sqrt(2)-2*1)*min(abs(xa-ya),abs(xb-yb)))
        def astarsearch(x, y):
            xx, xy = x
            world[xx][xy] = c.BLUE
            frontier = queue.PriorityQueue()
            frontier.put((0, x))
            came_from = {x: None}
            curr_cost = {x: 0}
            totalcost = 0
            while not frontier.empty():
                distance, point = frontier.get()
                if point == y:
                    totalcost = distance
                    a, b = y
                    world[a][b] = c.BLUE
                for i in getneighbors(point):
                    new_cost = curr_cost[x] + chebyshev(i, x)
                    if i not in curr_cost or new_cost < curr_cost[i]:
                        curr_cost[i] = new_cost
                        frontier.put((new_cost, i))
                        came_from[i] = x
            return totalcost

        def getColor(point, tribes):
            mini = random.randint(5, 16)
            x, y = point
            colored = c.WHITE
            topthree = []

            for i in tribes:
                tx, ty = i
                #cost = manhattan(i, point)
                cost = chebyshev(i, point)
                #cost = astarsearch(point, i)
                if cost < mini:
                    mini = cost
                    colored = world[tx][ty]
            return x, y, colored
        
        # tribes = int(self.x*self.y/1000*1.5)
        direction = [(0,1),(1,0),(0,-1),(-1,0)]
        colors = c.colors
        colors = sorted(colors, reverse=True)
        tribes = 4
        start = []
        world = deepcopy(self.world)
        ''' COLOR CURRENT MAP (WHITE BLACK) '''
        for i in range(len(world)):
            for j in range(len(world[i])):
                if world[i][j] > 0:
                    world[i][j] = c.WHITE
                elif world[i][j] == -6:
                    world[i][j] = c.WHITE
                    self.valid.append((i,j))
                else:
                    world[i][j] = c.BLACK

        locations = random.sample(self.valid, tribes)
        available = deepcopy(self.valid)
        print("LEN TILES: {} {}".format(len(available),type(available)))
        print(tileLen(len(available), type(available)))
        for i in range(tribes):
            x, y = available.pop(random.randint(0,len(available)))
            start.append((x,y))
            numCol = random.randint(0, len(colors))
            world[x][y] = colors[0]
            colors.pop(0)
        loop = 0
        print('AVA ', len(available))
        for i in range(len(available)):
            x, y, color = getColor(available.pop(), start)
            world[x][y] = color
            loop += 1
        print("LOOP", loop)
        print(astarsearch((70,40),(65, 42)))
        return world, self.valid, start
    def heightify(self):
        limits = namedtuple("Limits", ("l"))
        height = namedtuple("Height", ("h"))
        print(limits(self.lim))
        k = set()
        steps = {
                0: [0, -1],
                1: [0, 1],
                2: [-1, 0],
                3: [1, 0],
                }
        ry, rx = random.randint(3, self.y-4), random.randint(3, self.x-4)
        self.world[rx][ry] += 1
        self.valid.append((rx, ry))
        while self.lim > 0:
            step = steps[random.randint(0,3)]
            rx, ry = self.checkbounds(rx+step[0], ry+step[1])
            if self.world[rx][ry] == 0:
                self.world[rx][ry] = 1
                k.add(self.height[rx][ry])
                self.lim -= 1
                self.valid.append((rx, ry))
            self.height[rx][ry] += 1
            if self.height[rx][ry] > self.maxa:
                self.maxa = self.height[rx][ry]
              
        print(height(k))
    def removeIslands(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[0])):
                if self.world[i][j] == 0:
                    # water tile
                    if self.checkland(i, j):
                        self.world[i][j] == 1
    def checkland(self, x, y):
        lands = 1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i != x and j != y:
                    land = 1 if self.world[(x+i)%self.x][(y+j)%self.y] > 0 else 0
                    if land:
                        return 1
        return 0
    def addTemperature(self, size):
        lower, upper = (0, self.y) if size == 0 else (-self.y, self.y)
        k = set()
        
    def checkneighbors(self, x, y):
        total = 0
        for i in range(-1,2):
            for j in range(-1,2):
                total += 1 if self.world[(x+i)%self.x][(y+j)%self.y] <= 0 else 0
        return total

    def waterfy(self):
        water=namedtuple("Water", ("w"))
        k = set()
        for i in range(self.x):
            for j in range(self.y):
                if self.world[i][j] == 0:
                    self.world[i][j] = -self.checkneighbors(i,j)
                    k.add(self.world[i][j])
                    if self.world[i][j] < self.mini:
                        self.mini = self.world[i][j]
        print(water(k))
    def details(self):
        return self.world, self.valid, self.maxa, -self.mini

if __name__ == "__main__":
    world, valid, maxa, mini = Map(75, 200, .35).details()
    print(maxa, mini)
    lines = []
    for i in range(len(world)):
        line = ""
        for j in range(len(world[0])):
            line += GRN+"#"+END if (i, j) in valid else "."
        lines.append(line)
    print("\n".join(lines))
