#!/usr/bin/env python
import tdl
import math
import random
import symbols
import drunkards

def ellipse(scr, mapp):
    x, y = scr.get_size()
    def draw(cx, cy, xr, yr, mapp):
        t = 0
        step = 1
        group = set()
        mapp[cx][cy-yr] = '.'
        mapp[cx][cy-yr] = '.'
        mapp[cx-xr][cy] = '.'
        mapp[cx+xr][cy] = '.'
        while t <= 360:
            x = int(round(cx + xr*math.cos(t)))
            y = int(round(cy + yr*math.sin(t)))
            if (x,y) not in group:
                mapp[x][y] = '.'
                group.add((x,y))
            t += step
        return mapp, group
    
    cx, cy = x//2-1, y//2-1

    return draw(cx, cy, cx, cy, mapp)        

def circle(scr, mapp):
    x, y = scr.get_size()
    def draw(cx, cy, cr, mapp):
        valid = set()
        f = 1 - cr
        fx = 1
        fy = -2 * cr
        x = 0
        y = cr
        mapp[cx][cy-cr] = '.'
        mapp[cx][cy+cr] = '.'
        mapp[cx-cr][cy] = '.'
        mapp[cx+cr][cy] = '.'
        valid.add((cx,cy-cr))
        valid.add((cx,cy+cr))
        valid.add(cx,)
        while x < y:
            if f >= 0: 
                y -= 1
                fy += 2
                f += fy
            x += 1
            fx += 2
            f += fx    
            mapp[cx+x][cy+y] = '.'
            mapp[cx-x][cy+y] = '.'
            mapp[cx+x][cy-y] = '.'
            mapp[cx-x][cy-y] = '.'
            mapp[cx+y][cy+x] = '.'
            mapp[cx-y][cy+x] = '.'
            mapp[cx+y][cy-x] = '.'
            mapp[cx-y][cy-x] = '.'
        return mapp
    
    cx, cy = x//2-1, y//2-1
    cr = min(cx,cy)

    return draw(cx, cy, cr, mapp)




WIDTH, HEIGHT = 100, 80 # Defines the window size.

MOVEMENT_KEYS = {
                 'UP': [0, -1],
                 'DOWN': [0, 1],
                 'LEFT': [-1, 0],
                 'RIGHT': [1, 0],
                 'HOME': [-1, -1],
                 'PAGEUP': [1, -1],
                 'PAGEDOWN': [1, 1],
                 'END': [-1, 1],
                 'KP1': [-1, 1],
                 'KP2': [0, 1],
                 'KP3': [1, 1],
                 'KP4': [-1, 0],
                 'KP6': [1, 0],
                 'KP7': [-1, -1],
                 'KP8': [0, -1],
                 'KP9': [1, -1],
                 }




tdl.setFont('fonts/terminal12x12_gs_ro.png') # Configure the font.
console = tdl.init(WIDTH, HEIGHT, 'python-tdl tutorial')
x, y = console.get_size()
world = [['#' for i in range(y)] for j in range(x)]
#world = circle(console, world)
world, valid = ellipse(console, world)
# ellipse(console, world)
#world, valid = drunkards(console, 1300, world)
#playerX, playerY = valid[random.randint(0, len(valid)-1)]
playerX, playerY = 0, 0
color = (250,0,0)
last = ''
build = ''

house = [
    [symbols.chars['DTLCOR'],symbols.chars['DHLINE'], symbols.chars['DTRCOR']],
    [symbols.chars['DVLINE'],symbols.chars['SHOUSE'], symbols.chars['DVLINE']],
    [symbols.chars['DBLCOR'],symbols.chars['DHLINE'], symbols.chars['DBRCOR']]
]

while True: # Continue in an infinite game loop.
    console.clear() # Blank the console.
    # for i in range(16):
    #     for j in range(16):
    #         console.draw_char(j,i,i*16+j,(0,250,0))
    # symlist = symbols.chars.keys()
    # for i in range(len(symlist)):
    #     console.draw_char(i,1,symbols.chars[symlist[i]])
    for i in range(3):
        for j in range(3):
            console.draw_char(j,i,house[i][j],(200,50,250))
    '''
    for j in range(len(world)):
        for i in range(len(world[j])):
            if world[j][i] == '.':
                console.draw_char(j, i, '#',(0,250,0))
            else:
                console.draw_char(j, i, '.',(0,0,250))
    '''
    if (playerX, playerY) in console:
        console.draw_char(playerX, playerY, playerY*16+playerX, color)
        console.draw_str(20,2, "{} {}".format(playerX, playerY))
        console.draw_str(20,3, "{}".format(playerY*16+playerX))

    tdl.flush() # Update the window.
    for event in tdl.event.get(): # Iterate over recent events.
        if event.type == 'KEYDOWN':
            # We mix special keys with normal characters so we use keychar.
            if event.keychar.upper() in MOVEMENT_KEYS:
                # Get the vector and unpack it into these two variables.
                keyX, keyY = MOVEMENT_KEYS[event.keychar.upper()]
                # Then we add the vector to the current player position.
                if (playerX+keyX, playerY+keyY) in console:
                    playerX += keyX
                    playerY += keyY
            elif event.keychar.lower() == 'q':
                raise SystemExit('The window has been closed.')
        if event.type == 'QUIT':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')
