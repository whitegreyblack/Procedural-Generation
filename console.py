import mpd
import sys
import tdl
import numpy
import pprint

WIDTH, HEIGHT = 64, 64
mpd = mpd.MPD(WIDTH, HEIGHT, 1)
mpd.colorize()
pprint.pprint(numpy.matrix(mpd.map))
console = tdl.init(WIDTH+1, HEIGHT+1)

for i in range(WIDTH+1):
    for j in range(HEIGHT+1):
        val = mpd.map[i][j]
        console.draw_char(i, j, '#', (val, val, val))
        
tdl.flush()
tdl.event.keyWait()
del console