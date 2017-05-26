#!/usr/bin/env python
import tdl
import math
import copy
import color
import random
import symbols
import drunkards
''''
90380 100 60 40
77952 100 60 40
63035 100 60 40
78934 100 60 40
16732 120 60 40
55372 140 60 40
90209 140 60 35
39284 100 40 40
'''


WIDTH, HEIGHT = 480, 180 # Defines the window size.
XX, YY = 120, 45
TOOL_KEYS = {
             'd': '+',
             'h': '-',
             'v': '|',
             't': '^',
             'b': '8',
            }

HOT_KEYS = (
            'b',
            'd',
           )
MOVEMENT_KEYS = {
                 # standard arrow keys
                 'UP': [0, -1],
                 'DOWN': [0, 1],
                 'LEFT': [-1, 0],
                 'RIGHT': [1, 0],

                 # diagonal keys
                 # keep in mind that the keypad won't use these keys even if
                 # num-lock is off
                 'HOME': [-1, -1],
                 'PAGEUP': [1, -1],
                 'PAGEDOWN': [1, 1],
                 'END': [-1, 1],

                 # number-pad keys
                 # These keys will always show as KPx regardless if num-lock
                 # is on or off.  Keep in mind that some keyboards and laptops
                 # may be missing a keypad entirely.
                 # 7 8 9
                 # 4   6
                 # 1 2 3
                 'KP1': [-1, 1],
                 'KP2': [0, 1],
                 'KP3': [1, 1],
                 'KP4': [-1, 0],
                 'KP6': [1, 0],
                 'KP7': [-1, -1],
                 'KP8': [0, -1],
                 'KP9': [1, -1],
                 }

tdl.setFont('terminal8x12_gs_ro.png')
# tdl.setFont('4x6.png') # Configure the font.

# Create the root console.
console = tdl.init(XX, YY, 'python-tdl tutorial')

#x, y = console.get_size()
start = []
drunk = drunkards.Map(WIDTH, HEIGHT, .4, 21098)
world, valid, maxa, mini = drunk.details()
#world, valid, start = drunk.addClans()
print("MAXA:"+"{}".format(maxa))
print("MINI:"+"{}".format(mini))
playerX, playerY = 50, 25
num = 0
while True: # Continue in an infinite game loop.
    console.clear() # Blank the console.
    for i in range(XX):
        for j in range(YY):
            if world[i][j] > 0:
                console.draw_char(i,j, 'O', color.WHITE)
            else:
                console.draw_char(i,j, '.', world[i][j])
    for i in start:
        x, y = i
        console.draw_char(x, y, 'O', world[x][y])
    if (playerX, playerY) in valid:
        console.draw_char(playerX, playerY, 'X', (250,0,0))
        console.draw_str(1,1,"{} {} {}".format(playerX, playerY,
            world[playerX][playerY]))
    tdl.flush() # Update the window.
    for event in tdl.event.get(): # Iterate over recent events.
        if event.type == 'KEYDOWN':
            '''
            if event.key == 'ESCAPE':
                last = build = ''
                print("LAST  "+last)
                print("BUILD "+build)
            '''
            if event.keychar.upper() in MOVEMENT_KEYS:
                    keyX, keyY = MOVEMENT_KEYS[event.keychar.upper()]
                    if (playerX+keyX, playerY+keyY) in valid:
                        playerX += keyX
                        playerY += keyY
            if event.keychar.lower() == 'q':
                raise SystemExit('The window has been closed.')
            if event.keychar.lower() == 's':
                num -= 1
            if event.keychar.lower() == 'f':
                num += 1
        if event.type == 'QUIT':
            # Halt the script using SystemExit
            raise SystemExit('The window has been closed.')
