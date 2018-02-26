import random
import PIL
from generate.combinations import Sequences
from generate.base import Map, term_loop

class DrunkardsPeaks(Map):
    def __init__(self, width, height, limit, peaks, seed=None):
        """Drunkards algorithm with peaks"""
        super().__init__(width, height, seed)
        self.limit = int(width * height * limit)
        # print(width, height, limit, peaks)
        self.world = self.base_double_flat()
        self.world_normal = self.base_double_flat()
        self.world_colored = self.base_double_flat()

        x_lb = self.percentage(self.width, .3)
        x_hb = self.percentage(self.width, .7)
        y_lb = self.percentage(self.height, .3)
        y_hb = self.percentage(self.height, .7)

        self.peaks = [(
            random.randint(int(x_lb), int(x_hb)) , 
            random.randint(int(y_lb), int(y_hb))) 
            for _ in range(peaks)]
        # self.peaks = [(
        #     random.randint(width // 2 - width // 4, width // 2 + width // 4), 
        #     random.randint(height // 2 - height // 3, height // 2 + height // 3)) 
        #         for _ in range(peaks)]

        for px, py in self.peaks:
            self.world[py][px] = 5

        self.generate()

    def random_point(self):
        # return randint(0, self.x -1), randint(0, self.y - 1)
        return self.peaks[random.randint(0, len(self.peaks) - 1)]

    def generate(self):
        self.spaces = set()
        rx, ry = self.random_point()
        while len(self.spaces) <= self.limit:
            step = random.choice(list(Sequences.sequences(Sequences.LATERAL, inclusive=False)))
            if self.check_bounds(rx + step[0], ry + step[1]):
                rx, ry = rx + step[0], ry + step[1]
            else:
                rx, ry = self.random_point()

            self.world[ry][rx] += 1
            self.spaces.add((rx, ry))

        self.normalize()

class DrunkardsPeaksImproved(Map):
    def __init__(self, width, height, limit, peaks, seed=None):
        """Drunkards algorithm with peaks"""
        super().__init__(width, height, seed)
        self.limit = int(width * height * limit)
        # print(width, height, limit, peaks)
        self.world = self.base_double_flat()
        self.world_normal = self.base_double_flat()
        self.world_colored = self.base_double_flat()

        x_lb = self.percentage(self.width, .3)
        x_hb = self.percentage(self.width, .7)
        y_lb = self.percentage(self.height, .3)
        y_hb = self.percentage(self.height, .7)

        self.peaks = [(
            random.randint(int(x_lb), int(x_hb)) , 
            random.randint(int(y_lb), int(y_hb))) 
            for _ in range(peaks)]
        # self.peaks = [(
        #     random.randint(width // 2 - width // 4, width // 2 + width // 4), 
        #     random.randint(height // 2 - height // 3, height // 2 + height // 3)) 
        #         for _ in range(peaks)]

        for px, py in self.peaks:
            self.world[py][px] = 5

        self.generate()

def run_drunkards_peaks(width, height, noise, peaks, seed=None):
    m = DrunkardsPeaks(width, height, noise, peaks)
    m.normalize()
    m.evaluate()
    term_loop(m)

def run_combination(width, height, maps=5):
    m = DrunkardsPeaks(width, height, .45, 13)  

    m.generate()
    m.evaluate()

    term_loop(m)

def run_combination_image(width, height, maps=3):
    m = DrunkardsPeaks(width, height, limit=.35, peaks=10)
    # m = Drunkards(width, height, .45)
    m.evaluate()  
    m.output_image(colored=True, img_id='0')
    # n = m
    # n.smooth()
    # n.evaluate()  
    # n.output_image(colored=True, img_id='1')
    for i in range(maps - 1):
        n = DrunkardsPeaks(width, height, limit=.2, peaks=10)
        n.evaluate()
        n.output_image(colored=True, img_id=str((i + 1) * 2))
        m *= n
        m.evaluate()
        m.output_image(colored=True, img_id=str((i + 1) * 2 + 1))
        
    m.output_image(colored=False, img_id=str((i + 1) * 2 + 1) + 'c')

    for j in range(3):
        m.smooth()

    m.evaluate()
    m.output_image(colored=True, img_id=str((i + 1) * 2 + 2))
    m.output_image(colored=False,img_id=str((i + 1) * 2 + 2) + 'c')
    print(m.min)

def run_peaks_to_bitmap(width, height):
    assert width % 8 == 0 and height % 8 == 0
    m = DrunkardsPeaks(width, height, limit=.45, peaks=10)
    m.evaluate()
    print(m.world)
    

if __name__ == "__main__":
    print(__file__)
    run_combination_image(48, 36)
    # run_peaks_to_bitmap(480, 360)
