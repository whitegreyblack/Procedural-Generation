import math
import color
import random

pvar = "{}: {}"

''' initialize '''
WIDTH, HEIGHT = 20, 40

def randomfill(x, y, l, s=None): 
    """ Returns map filled with drunkards height algo """
    def smooth(world):
        return world
    seed = random.randint(0,99999)
    print(seed)
    random.seed(seed if seed else s)
    limit = int(x * y)
    print("limit: {}".format(limit))
    height = set()
    valid = set()
    world = [[-3 for i in range(y)] for j in range(x)] 
    print(limit)
    while len(valid) < limit:
        ry, rx = random.randint(0, y-1), random.randint(0, x-1)
        world[rx][ry] += 1
        valid.add((rx, ry))
        height.add(world[rx][ry])
        world[rx][ry]
    print(pvar.format('valid',len(valid)))
    return world, sorted(height, reverse=True)[0]

world, maxa = randomfill(WIDTH, HEIGHT, .5)
print(pvar.format('maxa', maxa))
pX, pY = WIDTH//2, HEIGHT//2

lines=[]
for i in range(len(world)):
    line = ""
    for j in range(len(world[i])):
        val = min((250//(maxa-1))*world[i][j]+2, 250)
        #console.draw_char(i, j, '.', (val, val, val))
        #print(i, j, '.')
        line += "." if val > 125 else " "
    lines.append(line)
print("\n".join(lines))
