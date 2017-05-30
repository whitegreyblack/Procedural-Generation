from PIL import Image, ImageDraw
import drunkards
import mpd
import dsa
import random
import randomfill
import multipleheight
from noise import pnoise2
from opensimplex import OpenSimplex
import diamondsquarewrapped
import pprint
import numpy

WIDTH, HEIGHT = 800, 800

img = Image.new('RGB', (WIDTH, HEIGHT))
ids = ImageDraw.Draw(img)

# drunk = drunkards.Map(HEIGHT, WIDTH, .55)
# for i in range(len(drunk.world[0])):
#     for j in range(len(drunk.world)):
#         val = drunk.world[j][i]
#         ids.point([i,j,i+1,j+1], val)

# mpd = mpd.MPD(WIDTH, HEIGHT, .5)
# mpd.colorize()
# for i in range(len(mpd.map[0])):
#     for j in range(len(mpd.map)):
#         val = mpd.map[j][i]
#         ids.point([j,i,j+1,i+1], val)

# dsa = dsa.DSA(WIDTH, HEIGHT, .55)
# dsa.colorize()
# for i in range(len(dsa.map[0])):
#     for j in range(len(dsa.map)):
#         val = dsa.map[j][i]
#         ids.point([j,i,j+1,i+1], val)

# mh, maxa = multipleheight.drunkards(WIDTH, HEIGHT, .55, 5)
# for i in range(len(mh[0])):
#     for j in range(len(mh)):
#         val = int((mh[j][i]/float(maxa[0]))*255)
#         # val = mh[j][i]
#         ids.point([i,j,i+1,j+1], (val, val, val))

# rf, maxa = randomfill.randomfill(HEIGHT, WIDTH, .55)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)

# for i in range(len(rf[0])):
#     for j in range(len(rf)):
#         val = int((rf[j][i]/float(maxa))*250)
#         ids.point([i,j,i+1,j+1], (val, val, val))

# octaves = 8
# # terrain = [[pnoise2(float(x)/HEIGHT,float(y)/WIDTH, octaves, 0.65, 6) for y in range(WIDTH)] for x in range(HEIGHT)]
# tmp=OpenSimplex()
# terrain = [[tmp.noise2d(float(x)/HEIGHT,float(y)/WIDTH) for y in range(WIDTH)] for x in range(HEIGHT)]

# mini, maxa = 0.0, 0.0
# for i in range(HEIGHT):
#     for j in range(WIDTH):
#         if terrain[i][j] < mini:
#             mini = terrain[i][j]
#         if terrain[i][j] > maxa:
#             maxa = terrain[i][j]
# print(mini, maxa)
# def color(val):
#     if 245 <= val:
#         return (250, 250, 250)
#     if 200 <= val < 245:
#         return (val/2, val/2, val/2)
#     elif 150 <= val < 200:
#         return (val/2, val, val/3)
#     elif 110 <= val < 150:
#         return (val, val, val/2)
#     elif 100 <= val < 110:
#         return (val, val, val)
#     else:
#         return (0, 5, val*5//3)

# def norm(x, mini, maxa):
#     return ((x-mini)/(maxa-mini))*250

# terrain = [[int(norm(terrain[x][y], mini, maxa)) for y in range(WIDTH)] for x in range(HEIGHT)]

# for i in range(len(terrain[0])):
#     for j in range(len(terrain)):
#         val = color(terrain[j][i])
#         ids.point([i, j, i+1, j+1], val)

# dsw = diamondsquarewrapped.DSW(WIDTH, HEIGHT, .55)
# dsw.normalizeAll()
# dsw.colorize()

# pprint.pprint(numpy.matrix(dsw.map))

# for j in range(HEIGHT):
#     for i in range(WIDTH):
#         val = dsw.map[i][j]
#         ids.point([i, j, i+1, j+1], (val,val, val))

img.save('map_{}_{}.png'.format(WIDTH, HEIGHT))