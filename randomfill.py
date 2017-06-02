import tdl
import math
import color
import copy
import random
import threading

pvar = "{}: {}"

def neighbor(x, y, world):
    total = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            #total += 1 if world[(x+i)%len(world)][(y+j)%len(world[0])] > 0 else 0\
            if (i, j) != (x, y):
                total += random.randint(
                    world[(x+i)%len(world)][(y+j)%len(world[0])]//2,
                    world[(x+i)%len(world)][(y+j)%len(world[0])]*2
                    )
    return total

def smooth(world, maxa):
    newmaxa = 0
    newworld = copy.deepcopy(world)
    print(pvar.format('incoming maxa', maxa))
    for k in range(1):
        for i in range(len(world)):
            for j in range(len(world[0])):
                try:
                    newworld[i][j] = neighbor(i, j, world)//(maxa)
                except:
                    print(neighbor(i,j, world))
                    raise
                if newworld[i][j] > newmaxa:
                    newmaxa = newworld[i][j]
    print(pvar.format("Maxa", newmaxa))
    return newworld, newmaxa

def randomfill(x, y, l, s=random.randint(0,99999), iter=0): 
    """ Returns map filled with drunkards height algo """
    random.seed(s)
    limit = int(x * y * l)
    height = set()
    valid = set()
    world = [[0 for i in range(y)] for j in range(x)] 
    while len(valid) < limit:
        ry, rx = random.randint(0, y-1), random.randint(0, x-1)
        world[rx][ry] += 1
        valid.add((rx, ry))
        height.add(world[rx][ry])
    print(height)
    height = sorted(height, reverse=True)[0]
    for x in range(iter):
        world, height = smooth(world, height)
    for i in range(len(world)):
        for j in range(len(world[0])):
            world[i][j] /= float(height)
    return world, height

def main():
    ''' initialize '''
    WIDTH, HEIGHT = 65, 65
    tdl.setFont('fonts/terminal8x12_gs_ro.png')
    console = tdl.init(WIDTH, HEIGHT, 'heightmap')
    world, maxa = randomfill(WIDTH, HEIGHT, .6, 999)

    print(pvar.format('maxa2', maxa))
    pX, pY = WIDTH//2, HEIGHT//2

    # 80 - 0|70, 10|60, 20|50, 30|40
    # 80 - 0|75, 5|70, 10|65, 15|60, 20|55, 25|50, 30|40

    worldflag=1
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
                        console.draw_char(i, j, '*', (0, val, val//3*2))
                    elif (maxa*2)/10 <= world[i][j] < (maxa*3)/10:
                        val = (world[i][j]*255/maxa)
                        console.draw_char(i, j, '*', (val*3, val*3, val/2))
                    elif (maxa)/10 <= world[i][j] < (maxa*2)/10:
                        val = max(250,(world[i][j]*255/maxa))
                        console.draw_char(i, j, '.', (val, val, val/2))
                    else:
                        val = max(250,(world[i][j]*255/maxa))
                        console.draw_char(i, j, '.', (0, val, val))                  
        tdl.flush()
        for event in tdl.event.get():
            if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'f'):
                worldflag *= -1
            if (event.type == 'KEYDOWN') and (event.keychar.lower() == 's'):
                world, maxa = smooth(world, maxa)
            if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'p'):
                print(world)
            if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
                raise SystemExit('The window has been closed.')
            if event.type == 'QUIT':
                raise SystemExit('The window has been closed.')

if __name__ == "__main__":
    main()