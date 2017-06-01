import random
import color

hvalues = {
    0: 0.05,
    1: 0.2,
    2: 0.4,
    3: 0.6,
    4: 0.8,
    5: 1.0
}

class HM:
    def __init__(self, size):
        self.size = size
        self.heat = [[x/float(size) for x in range(size)] for y in range(size)]
    
    def applyHeat(self, world):
        def norm(x, mina, maxi):
            return ((x-mina)/(maxi-mina))*255
            
        wmin, wmax = 0, 0
        mini, maxa = 0, 0

        for x in range(len(world)):
            for y in range(len(world[0])):
                wmin = world[x][y] if world[x][y] < wmin else wmin
                wmax = world[x][y] if world[x][y] > wmax else wmax

        for x in range(len(self.heat)):
            for y in range(len(self.heat[0])):
                # this model goes from cold(top) -> hot(bottom)'
                print(self.heat[x][y])
                print(norm(world[x][y], wmin, wmax))
                #                        0.0->1.0               0 -> 255
                self.heat[x][y] = self.heat[x][y] * norm(world[x][y], wmin, wmax)
                print(self.heat[x][y])
                mini = self.heat[x][y] if self.heat[x][y] < mini else mini
                maxa = self.heat[x][y] if self.heat[x][y] > maxa else maxa
        print('mi:', wmin,'ma',wmax)
        print('mi:', mini,'ma',maxa)


