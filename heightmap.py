import tdl
import math
import color
import random
import randomfill
"""
52666 40 20
21096 100 80
56330 100 80
"""

''' map functions '''
def drunkards(x, y, l, s=None): 
    """ Returns map filled with drunkards height algo """
    def checkbounds(tx, ty):
        if not 0 <= tx < int(x):
            tx = x//2
        if not 0 <= ty < int(y):
            ty = y//2
        return (tx, ty)
    steps = {
                0: [0, -1],
                1: [0, 1],
                2: [-1, 0],
                3: [1, 0],
            }
    seed = random.randint(0,99999)
    print(seed)
    random.seed(s if s else seed)
    limit = int(x * y * l)
    print("limit: {}".format(limit))
    height = set()
    valid = set()
    world = [[0 for i in range(y)] for j in range(x)]
    ry, rx = random.randint(0, y-1), random.randint(0, x-1)
    while len(valid) <= limit:
        step = steps[random.randint(0,3)]
        rx, ry = checkbounds(rx+step[0], ry+step[1])
        world[rx][ry] += 1
        valid.add((rx, ry))
    for i in range(len(world)):
        for j in range(len(world[i])):
            if world[i][j] == 43:
                print(i, j)
            if world[i][j] not in height:
                height.add(world[i][j])
    print(pvar.format('valid',len(valid)))
    return world, sorted(height, reverse=True)[0]

#world, maxa = randomfill(WIDTH, HEIGHT, .5)
world, maxa = drunkards(WIDTH, HEIGHT, .9)
print(pvar.format('maxa', maxa))
pX, pY = WIDTH//2, HEIGHT//2
worldflag = 1
while True:
    console.clear()
    for i in range(len(world)):
        for j in range(len(world[i])):
            if worldflag > 0:
                if (maxa*9)/10 <= world[i][j]:
                    console.draw_char(i, j, '^', color.WHITE)
                elif (maxa*8)/10 <= world[i][j] < (maxa*9)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, 'n', (val, val//2, val//3))
                elif (maxa*7)/10 <= world[i][j] < (maxa*8)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, 'n', (val, val//2, val//3*2))                  
                elif (maxa*5)/10 <= world[i][j] < (maxa*7)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, 30, (0, val, val//3))   
                elif (maxa*4)/10 <= world[i][j] < (maxa*5)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, 6, (0, val, val//3))
                elif (maxa*3)/10 <= world[i][j] < (maxa*4)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, '*', (0, val*3, val//3*2))
                elif (maxa)/10 <= world[i][j] < (maxa*3)/10:
                    val = (world[i][j]*255/maxa)
                    console.draw_char(i, j, '.', (val*3, val*3, val/2))
                # elif (maxa)/10 <= world[i][j] < (maxa*2)/10:
                #     val = max(250,(world[i][j]*255/maxa))
                #     console.draw_char(i, j, '.', (0, val//3*2, val))
                else:
                    val = max(250,(world[i][j]*255/maxa))
                    console.draw_char(i, j, '.', (0, val, val))
            else:
                if world[i][j] > 0:
                    console.draw_char(i, j, '.', (0, 150, 150))

    tdl.flush()
    for event in tdl.event.get():
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'f'):
            worldflag = worldflag * -1
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 's'):
            world, maxa = randomfill.smooth(world, maxa)
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'p'):
            print(world)
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
            raise SystemExit('The window has been closed.')

        if event.type == 'QUIT':
            raise SystemExit('The window has been closed.')
        