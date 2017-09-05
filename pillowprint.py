from PIL import Image, ImageDraw
import diamondsquareflat
import moisture
import randomfill
import heatmap
import random
import pprint
import color
import numpy


SIZE = 256

def value(x, y):
    return x*y

def heatify(val, maxa):
    if 0 <= val < value(.1, maxa):
        return color.HEAT_COLDEST
    elif value(0.1, maxa) <= val < value(.25, maxa):
        return color.HEAT_COLDER
    elif value(0.25, maxa) <= val < value(.50, maxa):
        return color.HEAT_COLD
    elif value(0.50, maxa) <= val < value(.75, maxa):
        return color.HEAT_WARM
    elif value(0.75, maxa) <= val < value(.90, maxa):
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
    # if value(.35, maxa) <= val:
    #     return (250, 250, 250)
    # else:
    #     return (5, 50, 250)
def islandfy(val, maxa):
    if value(.98, maxa) <= val: # mountains
        return (0, 100*4//3, 100*4//3)
    elif value(.88, maxa) <= val < value(.98, maxa):
        return (0, 110*5//3, 110*5//3)
    elif value(.78, maxa) <= val < value(.88, maxa): # green
        return (200/2, 200, 200/3)
    elif value(.58, maxa) <= val < value(.78, maxa):
        return (175/2, 175, 175/3)
    elif value(.29, maxa) <= val < value(.58, maxa):
        return (100/2, 100, 100/3)
    elif value(.21, maxa) <= val < value(.29, maxa):
        return (150, 150, 150)
    elif value(.19, maxa) <= val < value(.21, maxa):
        return (250, 230, 200)
    elif value(.02, maxa) <= val < value(.19, maxa): # water
        return (200, 200, 200)
    else:
        return (250, 250, 250)
def reverse(val, maxa):
    if val <= value(.02, maxa): # mountains
        # return (250, 250, 250)
        return (150, 150, 150)
    elif value(.02, maxa) <= val < value(.12, maxa):
        # return (200, 200, 200)
        return (150, 150, 150)
    elif value(.12, maxa) <= val < value(.20, maxa): # green
        return (150, 150, 150)
    elif value(.20, maxa) <= val < value(.22, maxa): # green
        return (150, 150, 150)
    elif value(.22, maxa) <= val < value(.40, maxa):
        # return (100/2, 100, 100/3)
        # return (0, 100*4//3, 100*4//3)
        return (150, 150, 150)
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
'''
octaves = 4
freq = 25.0 * octaves
#mapping = [[(snoise2(x/freq, y/freq, octaves, 0.5)*127)+128 for x in range(SIZE)] for y in range(SIZE)]
maxa = 0
for i in range(len(mapping)):
    for j in range(len(mapping[0])):
        if mapping[i][j] > maxa:
            maxa = mapping[i][j]
img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)
for j in range(SIZE):
    for i in range(SIZE):
        ids.point([i,j,i,j], heatify(255*(mapping[i][j]/maxa), 255))
img.save('noise.png')
'''
img = Image.new('RGB', (SIZE, SIZE))
imh = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)
idt = ImageDraw.Draw(imh)
OFFSET = 2
POWER = -.75
SEED = random.randint(0, 99999)
print(SEED)
height = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
height.initialize(1)
height.smooth()
h_norm = height.normalize(255)
pprint.pprint(numpy.matrix(h_norm))
for j in range(SIZE):
    for i in range(SIZE):
        # ids.point([i,j, i+1,j+1], islandfy(h_norm[i][j], 255))
        idt.point([i,j, i+1,j+1], colorize(h_norm[i][j], 255))
# img.save('heightR_{}_{}_{}_{}_{}.png'.format(height.seed, SIZE, SIZE, OFFSET, POWER))
imh.save('heightC_{}_{}_{}_{}_{}.png'.format(height.seed, SIZE, SIZE, OFFSET, POWER))

# # OFFSET = 3
# # POWER = -.55
# # SEED = random.randint(0, 999)
# # SEED = 200
# # print(SEED)
# # fractal = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
# # fractal.initialize(0)
# # f_norm = fractal.normalize(255)
# # pprint.pprint(numpy.matrix(f_norm))
# # for j in range(SIZE):
# #     for i in range(SIZE):
# #         ids.point([i,j, i+1,j+1], colorize(fractal.map[i][j], 255))
# # img.save('fractalB_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))
# img = Image.new('RGB', (SIZE, SIZE))
# ids = ImageDraw.Draw(img)

# FEATURE = 24.0
# simplex = OpenSimplex()
# fractal = [[(simplex.noise3d(x/FEATURE, y/FEATURE, 100.0)+1)*128 for x in range(SIZE)] for y in range(SIZE)]
# pprint.pprint(numpy.matrix(fractal))
# maxa = 0
# for i in range(len(fractal)):
#     for j in range(len(fractal[0])):
#         if fractal[i][j] > maxa:
#             maxa = fractal[i][j]
# f_norm = fractal
# for j in range(SIZE):
#     for i in range(SIZE):
#         val = fractal[i][j]/float(maxa)*255
#         ids.point([i,j, i+1,j+1], heatify(val, 255))
# img.save('noise.png')

img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)
heat = heatmap.HM(SIZE)
# mini, maxa = heat.vanilla()
heat.applyFractal(mapping)
heat.applyHeight(h_norm)
for j in range(SIZE):
    for i in range(SIZE):
        val = heatify(heat.heat[i][j], heat.maxa)
        ids.point([i, j, i+1, j+1], val)
img.save('heat.png')

# heat.applyHeight(h_norm)
# pprint.pprint(numpy.matrix(heat.heat))

# # mini, maxa, h_val = heat.applyHeight(h_norm)
# # COLUMNS, ROWS
# for j in range(SIZE):
#     for i in range(SIZE):
#         val = heatify(heat.heat[i][j], heat.maxa)
#         ids.point([i, j, i+1, j+1], val)
# img.save('heat_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))

# heat_map = heat.applyZone()
# # OFFSET = 2
# # POWER = -.25
# # SEED = random.randint(0, 999)
# # print(SEED)
# # fractal = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
# # fractal.initialize(0)
# # f_norm = fractal.normalize(255)

# # img = Image.new('RGB', (SIZE, SIZE))
# # ids = ImageDraw.Draw(img)
# rain = moisture.MM(f_norm)
# mini, maxa, r_val = rain.applyHeight(h_norm)
# # pprint.pprint(numpy.matrix(rain.rain))
# # COLUMNS, ROWS
# # for j in range(SIZE):
# #     for i in range(SIZE):
# #         val = heatify(rain.rain[i][j], maxa)
# #         ids.point([i, j, i+1, j+1], val)
# # img.save('rain_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))

# print(heat.heat[SIZE-1][0])
# print(heat.heat[0][SIZE-1])
# img = Image.new('RGB', (SIZE, SIZE))
# ids = ImageDraw.Draw(img)
# for i in range(SIZE):
#     for j in range(SIZE):
#         #val = color.BIOMES[r_val[i][j]][h_val[i][j]] if h_norm[i][j] > value(.19,255) else colorize(h_norm[i][j], 255)
#         val = color.BIOMES[heat_map[i][j]][3] if heat.heat[i][j] > .5 else colorize(heat.heat[i][j], 1)
#         ids.point([i, j, i+1, j+1], val)
# img.save('all_{}_{}_{}_{}_{}.png'.format(SEED, SIZE, SIZE, OFFSET, POWER))
