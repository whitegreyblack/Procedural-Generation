from PIL import Image, ImageDraw
import diamondsquareflat
import heatmap
import random
import pprint
import color
import numpy

WIDTH, HEIGHT = 64, 64
SIZE = 17

def value(x, y):
    return int(round(x*y))

def colorize(val):
    # return (val, val, val) 
    if 250 <= val: # mountains
        return (250, 250, 250)
    elif 225 <= val < 250:
        return (200, 200, 200)
    elif 200 <= val < 225: # green
        return (150, 150, 150)
    elif 150 <= val < 200:
        return (100/2, 100, 100/3)
    elif 125 <= val < 150:
        return (175/2, 175, 175/3)
    elif 105 <= val < 125:
        return (200/2, 200, 200/3)
    elif 100 <= val < 105:
        return (250, 230, 200)
    elif 50 <= val < 100: # water
        return (0, 110*5//3, 110*5//3) 
    else:
        return (0, 100*4//3, 100*4//3)

# img = Image.new('RGB', (SIZE*2-1, SIZE))
    # ids = ImageDraw.Draw(img)

    # OFFSET = 2.5
    # POWER = -.5
    # SEED = random.randint(0, 999)
    # print(SEED)

    # dsw = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
    # dsw.initialize(1)
    # dsw.smooth()

    # # COLUMNS, ROWS

    # for j in range(SIZE):
    #     for i in range(SIZE):
    #         val = colorize(dsw.map[i][j])
    #         ids.point([i, j, i+1, j+1], val)

    # SEED = random.randint(0, 999)
    # copy = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
    # print('len',len(dsw.rget()))
    # copy.lset(dsw.rget())
    # copy.initialize(1)
    # # rows
    # for j in range(SIZE):
    #     # columns
    #     for i in range(SIZE):
    #         ids.point([SIZE+i-1,j,SIZE+i,j+1], colorize(copy.map[i][j]))

    # img.save('{}_{}_{}_{}_{}.png'.format(dsw.seed, SIZE, SIZE, OFFSET, POWER))

def heatify(val):
    if 0 <= val < value(.05, 255):
        return color.HEAT_COLDEST
    elif value(0.05, 255) <= val < value(.2, 255):
        return color.HEAT_COLDER
    elif value(0.2, 255) <= val < value(.4, 255):
        return color.HEAT_COLD
    elif value(0.4, 255) <= val < value(.6, 255):
        return color.HEAT_WARM
    elif value(0.6, 255) <= val < value(.8, 255):
        return color.HEAT_WARMER
    else:
        return color.HEAT_WARMEST

img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)

OFFSET = 1.25
POWER = -.4
SEED = random.randint(0, 999)
print(SEED)

dsw = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
dsw.initialize(1)
for j in range(SIZE):
    for i in range(SIZE):
        ids.point([i,j, i+1,j+1], colorize(dsw.map[i][j]))
img.save('{}_{}_{}_{}_{}.png'.format(dsw.seed, SIZE, SIZE, OFFSET, POWER))


img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)
heat = heatmap.HM(SIZE)
heat.applyHeat(dsw.map)

# COLUMNS, ROWS
for j in range(SIZE):
    for i in range(SIZE):
        val = heatify(heat.heat[i][j])
        ids.point([i, j, i+1, j+1], val)

img.save('heat_{}_{}_{}_{}_{}.png'.format(dsw.seed, SIZE, SIZE, OFFSET, POWER))
