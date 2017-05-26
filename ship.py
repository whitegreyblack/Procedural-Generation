#!/usr/bin/env python
import tdl
import sys
import math
import color
import random
import ellipse
import symbols
from prefab import cabin
WIDTH, HEIGHT = 0, 0

class Ship:
    def __init__(self, x, y, cells, seed=None):
        pass

def main():
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



    ship = [[0 for i in range(HEIGHT)] for j in range(WIDTH)]
    tdl.setFont('terminal12x12_gs_ro.png') # Configure the font.
    console = tdl.init(WIDTH, HEIGHT, 'python-tdl tutorial')
    ship, group = ellipse.Ellipse(console, ship)
    x, y = console.get_size()
    playerX, playerY = 1,1
    while True:
        console.clear()

        for i in range(WIDTH):
            for j in range(HEIGHT):
                if ship[i][j] == '.':
                    console.draw_char(i, j, '.', color.WHITE)
        
        for k in range(3):
            for j in range(len(cabin.prefab)):
                for i in range(len(cabin.prefab[0])):
                    console.draw_char(i+k*5+45, j+35, symbols.chars[cabin.prefab[j][i]])

        for k in range(3):
            for j in range(len(cabin.prefab)):
                for i in range(len(cabin.prefab[0])):
                    console.draw_char(i+k*5+45, j+6+35, symbols.chars[cabin.prefab[j][i]])

        if (playerX, playerY) in console:
            console.draw_char(playerX, playerY, '@', color.RED)

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing System Arg #2")
        print("  USAGE: py ship.py [# of thrusters]")
        exit(-1)
    else:
        main()