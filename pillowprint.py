from PIL import Image, ImageDraw
import diamondsquareflat
import moisture
import randomfill
import heatmap
import random
import pprint
import color
import numpy

SIZE = 257

def value(x, y):
    return x*y

def heatify(val, maxa):
    if 0 <= val < value(.4, maxa):
        return color.HEAT_COLDEST
    elif value(0.4, maxa) <= val < value(.6, maxa):
        return color.HEAT_COLDER
    elif value(0.6, maxa) <= val < value(.75, maxa):
        return color.HEAT_COLD
    elif value(0.75, maxa) <= val < value(.85, maxa):
        return color.HEAT_WARM
    elif value(0.85, maxa) <= val < value(.95, maxa):
        return color.HEAT_WARMER
    else:
        return color.HEAT_WARMEST

def fractify(val, maxa):
    if val < value(.15, maxa):
        return color.HEAT_COLDEST
    elif value(0.15, maxa) <= val < value(.25, maxa):
        return color.HEAT_COLDER
    elif value(0.25, maxa) <= val < value(.35, maxa):
        return color.HEAT_COLD
    elif value(0.35, maxa) <= val < value(.45, maxa):
        return color.HEAT_WARM
    elif value(0.45, maxa) <= val < value(.5, maxa):
        return color.HEAT_WARMER
    else:
        return color.HEAT_WARMEST

def colorize(val, maxa):
    if value(.98, maxa) <= val: # mountains
        return (250, 250, 250)
    elif value(.88, maxa) <= val < value(.98, maxa):
        return (200, 200, 200)
    elif value(.78, maxa) <= val < value(.88, maxa): # green
        return (150, 150, 150)
    elif value(.58, maxa) <= val < value(.78, maxa):
        return (100/2, 100, 100/3)
    elif value(.29, maxa) <= val < value(.58, maxa):
        return (175/2, 175, 175/3)
    elif value(.21, maxa) <= val < value(.29, maxa):
        return (200/2, 200, 200/3)
    elif value(.19, maxa) <= val < value(.21, maxa):
        return (250, 230, 200)
    elif value(.02, maxa) <= val < value(.19, maxa): # water
        return (0, 110*5//3, 110*5//3) 
    else:
        return (0, 100*4//3, 100*4//3)

def reverse(val, maxa):
    if val <= value(.02, maxa): # mountains
        return (250, 250, 250)
    elif value(.02, maxa) <= val < value(.12, maxa):
        return (200, 200, 200)
    elif value(.12, maxa) <= val < value(.20, maxa): # green
        return (150, 150, 150)
    elif value(.20, maxa) <= val < value(.22, maxa): # green
        return (250, 230, 200)
    elif value(.22, maxa) <= val < value(.40, maxa):
        # return (100/2, 100, 100/3)
        return (0, 100*4//3, 100*4//3)
    elif value(.40, maxa) <= val < value(.42, maxa): # green
        return (250, 230, 200)
    elif value(.42, maxa) <= val < value(.71, maxa):
        return (175/2, 175, 175/3)
    elif value(.71, maxa) <= val < value(.79, maxa):
        return (200/2, 200, 200/3)
    elif value(.79, maxa) <= val < value(.81, maxa):
        return (250, 230, 200)
    elif value(.98, maxa) <= val < value(.81, maxa): # water
        return (0, 110*5//3, 110*5//3) 
    else:
        return (0, 100*4//3, 100*4//3)

# img = Image.new('RGB', (SIZE, SIZE))
imh = Image.new('RGB', (SIZE, SIZE))
# ids = ImageDraw.Draw(img)
idt = ImageDraw.Draw(imh)
OFFSET = 2.5
POWER = -.5
SEED = random.randint(0, 999)
print(SEED)
height = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
height.initialize(1)
h_norm = height.normalize(255)
for j in range(SIZE):
    for i in range(SIZE):
        # ids.point([i,j, i+1,j+1], reverse(h_norm[i][j], 255))
        idt.point([i,j, i+1,j+1], colorize(h_norm[i][j], 255))
# img.save('heightR_{}_{}_{}_{}_{}.png'.format(height.seed, SIZE, SIZE, OFFSET, POWER))
imh.save('heightC_{}_{}_{}_{}_{}.png'.format(height.seed, SIZE, SIZE, OFFSET, POWER))

OFFSET = 3
POWER = -.35
SEED = random.randint(0, 999)
print(SEED)
fractal = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
fractal.initialize(0)
f_norm = fractal.normalize(255)
# for j in range(SIZE):
#     for i in range(SIZE):
#         ids.point([i,j, i+1,j+1], colorize(fractal.map[i][j], 255))
# img.save('fractalB_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))

# img = Image.new('RGB', (SIZE, SIZE))
# ids = ImageDraw.Draw(img)
heat = heatmap.HM(SIZE)
mini, maxa = heat.applyFractal(f_norm)
mini, maxa, h_val = heat.applyHeight(h_norm)
# COLUMNS, ROWS
# for j in range(SIZE):
#     for i in range(SIZE):
#         val = heatify(heat.heat[i][j], maxa)
#         ids.point([i, j, i+1, j+1], val)
# img.save('heat_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))

# OFFSET = 2
# POWER = -.25
# SEED = random.randint(0, 999)
# print(SEED)
# fractal = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
# fractal.initialize(0)
# f_norm = fractal.normalize(255)

# img = Image.new('RGB', (SIZE, SIZE))
# ids = ImageDraw.Draw(img)
rain = moisture.MM(f_norm)
mini, maxa, r_val = rain.applyHeight(h_norm)
pprint.pprint(numpy.matrix(rain.rain))
# COLUMNS, ROWS
# for j in range(SIZE):
#     for i in range(SIZE):
#         val = heatify(rain.rain[i][j], maxa)
#         ids.point([i, j, i+1, j+1], val)
# img.save('rain_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))



img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)
for i in range(SIZE):
    for j in range(SIZE):
        val = color.BIOMES[r_val[i][j]][h_val[i][j]] if h_norm[i][j] > value(.19,255) else colorize(h_norm[i][j], 255)
        ids.point([i, j, i+1, j+1], val)
img.save('all_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))