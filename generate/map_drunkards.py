import random
from combinations import Sequences
from base import Map, term_loop

class Drunkards(Map):
    def __init__(self, width, height, limit, seed=None):
        super().__init__(width=width, height=height, seed=seed)
        self.limit = int(height * width * limit)

        self.world = self.base_double_flat()
        self.world_normal = self.base_double_flat()
        self.world_colored = self.base_double_flat()

        self.generate()

    def generate(self): 
        """ Returns map filled with drunkards height algo """
        self.spaces = set()
        ry, rx = self.random_point()

        while len(self.spaces) <= self.limit:
            step = random.choice(list(Sequences.sequences(Sequences.LATERAL, inclusive=False)))
            # if at somepoint we are at the edge of the map and choose
            # a point outside of the map bounds we choose a random point
            # from the map to start the process again
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        self.normalize()

def run_drunkards(width, height, noise, seed=None):
    m = Drunkards(width, height, noise, seed)
    m.normalize()
    m.evaluate()
    term_loop(m)

if __name__ == "__main__":
    print(__file__)