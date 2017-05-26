import tdl
import math
import color
import graph
import random
import movement

pvar = "{}: {}"

''' initialize '''
WIDTH, HEIGHT = 240, 90
tdl.setFont('terminal8x12_gs_ro.png')
#tdl.setFont('4x6.png')
console = tdl.init(WIDTH, HEIGHT, 'heightmap')
px, py = WIDTH//2, HEIGHT//2

world = graph.Graph('world', WIDTH, HEIGHT)
world.midpoint(.6)
valid, maxa = world.drunkards(.6)
world.setTiles(maxa)
print(world.world[WIDTH//2][HEIGHT//2].height)
print(world.seed)
print(maxa)
flag = 1
while True:
    console.clear()
    for i in range(world.width):
        for j in range(world.height):
            #fg =  max(world.world[i][j].variance * 125.0 + 125.0, 250)
            console.draw_char(i, j, world.world[i][j].symbol, world.world[i][j].foreground)
    if (px, py):
        console.draw_char(px, py, '@', color.WHITE)

    tdl.flush()
    for event in tdl.event.get():
        if (event.type =='KEYDOWN') and (event.keychar.upper() in movement.KEYS):
            a, b = movement.KEYS[event.keychar.upper()]
            if (px+a, py+b) in console:
                px, py = px+a, py+b
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 's'):
            maxa = world.smooth(maxa)
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'f'):
            flag = flag * -1
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'c'):
            world.setTiles(maxa)
        if (event.type == 'KEYDOWN') and (event.keychar.lower() == 'q'):
            raise SystemExit('The window has been closed.')
        if event.type == 'QUIT':
            raise SystemExit('The window has been closed.')