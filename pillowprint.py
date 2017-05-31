from PIL import Image, ImageDraw
import diamondsquareflat
import random
import pprint
import numpy

WIDTH, HEIGHT = 64, 64
SIZE = 64
# img = Image.new('RGB', (WIDTH+1, HEIGHT+1))

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
def color(val): 
    if 215 <= val: # mountains
        return (250, 250, 250)
    elif 200 <= val < 215:
        return (200, 200, 200)
    elif 175 <= val < 200: # green
        return (150, 150, 150)
    elif 150 <= val < 175:
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

# def norm(x, mini, maxa):
#     return ((x-mini)/(maxa-mini))*250

# terrain = [[int(norm(terrain[x][y], mini, maxa)) for y in range(WIDTH)] for x in range(HEIGHT)]

# for i in range(len(terrain[0])):
#     for j in range(len(terrain)):
#         val = color(terrain[j][i])
#         ids.point([i, j, i+1, j+1], val)

img = Image.new('RGB', (SIZE*2, SIZE))
ids = ImageDraw.Draw(img)
SEED = random.randint(0, 999)
print(SEED)
OFFSET = 2.5
POWER = -.3
dsw1 = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
dsw2 = diamondsquareflat.DS(SIZE, 255, seed=SEED, offset=OFFSET, power=POWER)
dsw1.initialize(1)
dsw2.initialize(1, b=dsw1.map[0][SIZE-1], c=dsw1.map[SIZE-1][SIZE-1])
for j in range(SIZE):
    for i in range(SIZE):
        val = color(dsw1.map[i][j])
        ids.point([i, j, i+1, j+1], val)
for j in range(SIZE):
    for i in range(SIZE):
        val = color(dsw2.map[i][j])
        ids.point([SIZE+i, j, SIZE+i+1, j+1], val)
img.save('map3B_{}_{}_{}_{}_{}.png'.format(dsw1.seed, SIZE, SIZE, OFFSET, POWER))