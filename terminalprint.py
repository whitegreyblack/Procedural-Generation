import sys
import tdl
import numpy
import pprint
import drunkards
import randomfill
import multipleheight
import dsa
import mpd
WIDTH, HEIGHT = 64, 64
console = tdl.init(WIDTH, HEIGHT)

# drunk = drunkards.Map(WIDTH, HEIGHT, .55)
# pprint.pprint(numpy.matrix(drunk.world))
# for i in range(WIDTH):
#     for j in range(HEIGHT):
#         val = drunk.world[i][j]
#         console.draw_char(i, j, '#', (val, val, val))

# mh, maxa = multipleheight.drunkards(WIDTH, HEIGHT, .55, 5)
# print(maxa[0])
# pprint.pprint(numpy.matrix(mh))
# for i in range(WIDTH):
#     for j in range(HEIGHT):
#         print(mh[i][j])
#         # val = int((mh[i][j]/float(maxa[0]))*250)
#         val = mh[i][j]
#         console.draw_char(i, j, '#', (val, val, val))

# rf, maxa = randomfill.randomfill(WIDTH, HEIGHT, .55)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)
# rf, maxa = randomfill.smooth(rf, maxa)

# for i in range(len(rf[0])):
#     for j in range(len(rf)):
#         val = int((rf[j][i]/float(maxa))*250)
#         console.draw_char(i, j, '#', (val, val, val))

mpd = mpd.MPD(WIDTH, HEIGHT, 50)
mpd.colorize()

for i in range(WIDTH):
    for j in range(HEIGHT):
        val = mpd.map[i][j]
        console.draw_char(i, j, '#', (val, val, val))

tdl.flush()
tdl.event.keyWait()
del console
