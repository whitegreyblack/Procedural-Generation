import random
from base import Map, key_handle_exit
from bearlibterminal import terminal

class MPD(Map):
    def __init__(self, width, height, noise, seed=None):
        super().__init__(width=width, height=height, seed=seed)
        self.noise = noise
        self.world = self.base_single_float()

    def subdivide(self, x1, x2, delta):
        if x1 + 1 == x2:
            return

        x3 = (x1 + x2) // 2
        dy = (random.random() * 2 - 1) * delta

        # midpoint
        self.world[x3] = (self.world[x1] + self.world[x2] + self.world[x3]) / 3 + dy

        self.subdivide(x1, x3, delta * self.noise)
        self.subdivide(x3, x2, delta * self.noise)

def run_midpoint_single(width, height, noise=.7, seed=None):
    terminal.open()

    line = MPD(width=width, height=height, noise=noise, seed=seed)
    line.subdivide(0, width - 1, 50)
    
    line.minmax_single()

    total = line.max - line.min
    print(total, line.max, line.min)

    while True:
        terminal.clear()

        for i in range(width):
            terminal.puts(i, int(round((line.world[i] - line.min)) / (total) * height), '.')

        terminal.refresh()

        key = terminal.read()

        if key_handle_exit(key):
            terminal.close()
            break

        elif key == terminal.TK_S:
            line.smooth_single()

if __name__ == "__main__":
    w, h = 240, 160
    print(__file__)
    run_midpoint_single(w, h)