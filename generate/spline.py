from PIL import Image, ImageDraw
import random
import pprint
import color
import numpy

SIZE = 128
world = [[0 for x in range(SIZE)] for y in range(SIZE)]

[random.randint(0, SIZE-1), 0, ]


start = [
    [0,0, SIZE-1, SIZE-1, (0,0,250)], 
    [SIZE-1,0, 0, SIZE-1, (0,250,0)],
    [0,SIZE-1, SIZE-1, 0, (250,0,0)],
    [SIZE-1,SIZE-1, 0, 0, (90,5,90)]
    ]

img = Image.new('RGB', (SIZE, SIZE))
ids = ImageDraw.Draw(img)

for i in range(len(start)):
    sx, sy, ex, ey, col = start[i]
    mx, my = (ex-sx)/(SIZE-1), (ey-sy)/(SIZE-1)
    lx, ly, hx, hy = min(sx, ex), min(sy, ey), max(sx, ex), max(sy, ey)
    print(mx, my)
    ids.point([sx,sy,sx,sy], col)
    while lx <= sx <= hx and ly <= sy <= hy:
        sx += mx if random.randint(0, 1) else 0
        sy += my if random.randint(0, 1) else 0
        ids.point([sx,sy,sx,sy], col)

img.save('spline.png')
