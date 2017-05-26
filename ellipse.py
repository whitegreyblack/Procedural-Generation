import math

def Ellipse(scr, mapp):
    x, y = scr.get_size()
    def draw(cx, cy, xr, yr, mapp):
        t = 0
        step = 1
        group = set()
        mapp[cx][cy-yr] = '.'
        mapp[cx][cy-yr] = '.'
        mapp[cx-xr][cy] = '.'
        mapp[cx+xr][cy] = '.'
        while t <= 360:
            x = int(round(cx + xr*math.cos(t)))
            y = int(round(cy + yr*math.sin(t)))
            if (x,y) not in group:
                mapp[x][y] = '.'
                group.add((x,y))
            t += step
        return mapp, group
    
    cx, cy = x//2-1, y//2-1

    return draw(cx, cy, cx, cy, mapp)        