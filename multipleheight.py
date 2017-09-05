import tdl
import math
import color
import random
import randomfill

''' map functions '''
def drunkards(x, y, l, peaks, s=None): 
    """ Returns map filled with drunkards height algo """
    steps = {
            0: [0, -1],
            1: [0, 1],
            2: [-1, 0],
            3: [1, 0],
        }
    points = [(random.randint(x/2-x/4,x/2+x/4),random.randint(y/2-y/3,y/2+y/3)) for i in range(peaks)]

    def checkbounds(tx, ty):
        if not 0 <= tx < int(x):
            return points[random.randint(0, len(points)-1)]
        if not 0 <= ty < int(y):
            return points[random.randint(0, len(points)-1)]
        return (tx, ty)

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
            if world[i][j] not in height:
                height.add(world[i][j])

    return world, sorted(height, reverse=True)

if __name__ == "__main__":

    pvar = "{}: {}"

    ''' initialize '''
    WIDTH, HEIGHT = 240, 90
    tdl.setFont('fonts/terminal8x12_gs_ro.png')
    console = tdl.init(WIDTH, HEIGHT, 'heightmap')
    #world, maxa = randomfill(WIDTH, HEIGHT, .5)
    world, maxa = drunkards(WIDTH, HEIGHT, .9, 4)
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
                        console.draw_char(i, j, '*', (val/2, val, val/2))
                    elif (maxa)/10 <= world[i][j] < (maxa*3)/10:
                        val = (world[i][j]*255/maxa)
                        console.draw_char(i, j, 'o', (val*2, val*3, val/2))
                    else:
                        val = max(250,(world[i][j]*255/maxa))
                        console.draw_char(i, j, '~', (0, val, val))
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
        
