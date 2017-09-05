import random
import color
import copy

steps = {
    0: [0,-1],
    1: [0,1],
    2: [-1,0],
    3: [1, 0],
    4: [-1,-1],
    5: [-1,1],
    6: [1,-1],
    7: [1,1],
}

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heat = 0
        self.mask = 0
        self.height = 0
        self.moisture = 0

class Tile:
    def __init__(self, x, y, symbol=None):
        self.x = x
        self.y = y
        self.symbol = '.' if not symbol else symbol
        self.height = 0
        self.foreground = color.WHITE
        self.background = color.BLACK
        self.variance = 0
    
    def __repr__(self):
        return """Tile [{}]: ({} {}), {}, {}, {}""".format( self.symbol,
            self.x, self.y, self.height, self.foreground, self.background
        )

    def getColor(self, x):
        r, g, b = self.foreground if x == 1 else self.background
        return (r, g, b)

    def __add__(self, other):
        if isinstance(other, Tile):
            r1, g1, b1 = self.getColor(1)
            r2, g2, b2 = other.foreground
            self.height = (self.height+other.height)/2
            self.foreground = ((r1+r2)/2,(g1+g2)/2,(b1+b2)/2)
        return self

    def __iadd__(self, other):
        if isinstance(other, Tile):
            r1, g1, b1 = self.getColor(1)
            r2, g2, b2 = other.foreground
            self.height = (self.height+other.height)/2
            print(self.height)
            self.foreground = ((r1+r2)/2,(g1+g2)/2,(b1+b2)/2)
        elif isinstance(other, list):
            if all([isinstance(i, Tile) for i in other]):
                for i in other:
                    self.__iadd__(i)
        return self

class Graph:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.createWorld()

    def createWorld(self):
        self.world = []
        self.tiles = set()
        for i in range(self.width):
            column = []
            for j in range(self.height):
                column.append(Tile(i, j))
                self.tiles.add((i, j))
            self.world.append(column)

    def setTile(self, x, y, s=None, fg=None, bg=None):
        if self.world and 0 <= x < self.width and 0 <= y < self.height:
            self.world[x][y].symbol = s if s else '.'
            self.world[x][y].foreground = fg if fg else color.BLACK
            self.world[x][y].background = bg if bg else color.BLACK
            
    def setTiles(self, maxa):
        for i in range(self.width):
            for j in range(self.height):
                if (maxa*9)/10 <= self.world[i][j].height:
                    self.setTile(i, j, '^', color.WHITE)
                elif (maxa*7)/10 <= self.world[i][j].height < (maxa*9)/10:
                    val = (self.world[i][j].height*255/maxa)
                    self.setTile(i, j, 'n', (val, val//2, 
                        random.randint(val//3, val//3*2)))
                elif (maxa*4)/10 <= self.world[i][j].height < (maxa*7)/10:
                    val = (self.world[i][j].height*255/maxa)
                    self.setTile(i, j, random.choice([30,'*',7]),
                        (0, val, random.randint(val//3, val//3*2)))
                elif (maxa)/10 <= self.world[i][j].height < (maxa*4)/10:
                    val = (self.world[i][j].height*255/maxa)
                    self.setTile(i, j, '.', (val*2, val*2, val//2))
                else:
                    val = (self.world[i][j].height*255/maxa)
                    self.setTile(i, j, '~', (0, 50, 125))

    def neighbor(self, x, y):
        total = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i, j) != (x, y):
                    total += random.randint(
                        self.world[(x+i)%self.width][(y+j)%self.height].height//2,
                        self.world[(x+i)%self.width][(y+j)%self.height].height*2
                        )
        return total

    def smooth(self, maxa):
        newmaxa = 0
        newworld = copy.deepcopy(self.world)
        height = set()
        for i in range(self.width):
            for j in range(self.height):
                newworld[i][j].height = self.neighbor(i, j)//maxa
                if newworld[i][j].height > newmaxa:
                    newmaxa = newworld[i][j].height
        self.world = newworld
        print('maxa', newmaxa)
        return newmaxa

    def midpoint(self, l, s=None):
        self.seed = s if s else random.randint(0, 9999)
        random.seed(self.seed)
        for i in range(self.width):
            for j in range(self.height):
                self.world[i][j].variance = random.uniform(-1, 1)

    def drunkards(self, l, s=None):
        def bound(x, y):
            if not 0 <= x < self.width:
                if random.randint(0, 2) == 1:
                    x = random.randint(0, self.width-1)
                else:
                    x = self.width//2
            if not 0 <= y < self.height:
                if random.randint(0, 2) == 1:
                    y = random.randint(0, self.height-1)
                y = self.height//2
            return x, y

        self.seed = s if s else random.randint(0, 9999) 
        random.seed(self.seed)
        limit = int(self.width * self.height * l)
        height, valid = set(), set()

        rx = random.randint(0, self.width)
        ry = random.randint(0, self.height)

        while len(valid) <= limit:
            step = steps[random.randint(0, len(steps.keys())-1)]
            rx, ry = bound(rx+step[0], ry+step[1])
            self.world[rx][ry].height += 1
            valid.add((rx, ry))
            
        for i in range(self.width):
            for j in range(self.height):
                height.add(self.world[i][j].height)

        return valid, sorted(height, reverse=True)[0]
