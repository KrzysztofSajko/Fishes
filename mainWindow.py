import pyglet
import math
from graphics.fish import Violet, Shark, Species, FishStats


class Stats:
    def __init__(self, x, y, batch, group):
        self.shark_q = 0
        self.violet_q = 0
        self.shark_label = pyglet.text.Label(f"Sharks: {self.shark_q}", x=x, y=y, batch=batch, group=group)
        self.violet_label = pyglet.text.Label(f"Violets: {self.violet_q}", x=x, y=y+20, batch=batch, group=group)

    def update(self):
        self.shark_label.text = f"Sharks: {self.shark_q}"
        self.violet_label.text = f"Violets: {self.violet_q}"



class MainWindow(pyglet.window.Window):
    def __init__(self):
        # setup window
        super().__init__(width=1280, height=720, caption="Woobly fishes wooblying")
        pyglet.gl.glClearColor(0.06, 0.06, 0.06, 1)
        self.set_location(120, 60)
        self.background = None
        # create main batch and groups
        self.batch = pyglet.graphics.Batch()
        self.g_background = pyglet.graphics.OrderedGroup(0)
        self.g_fishes = pyglet.graphics.OrderedGroup(1)
        self.g_stats = pyglet.graphics.OrderedGroup(2)
        # create additional elements
        self.stats = Stats(5, 5, batch=self.batch, group=self.g_stats)
        # fishes quantities
        self.violets = []
        self.sharks = []
        self.setup()

    def setup(self):
        # load background
        bg = pyglet.image.load("sprites/underwater_bcg.png")
        self.background = pyglet.sprite.Sprite(bg, 0, 0, batch=self.batch, group=self.g_background)
        self.background.scale_x = self.width / bg.width
        self.background.scale_y = self.height / bg.height
        # set stats
        self.stats.shark_q = Species.Shark.stats[FishStats.start_pop]
        self.stats.violet_q = Species.Violet.stats[FishStats.start_pop]
        # create fishes
        win_info = dict(batch=self.batch, group=self.g_fishes, width=self.width, height=self.height)
        for i in range(Species.Violet.stats[FishStats.start_pop]):
            self.violets.append(Violet(win_info))
        for i in range(Species.Shark.stats[FishStats.start_pop]):
            self.sharks.append(Shark(win_info))

    def draw(self):
        self.clear()
        self.batch.draw()

    def update(self, dt):
        for violet in self.violets:
            violet.update(dt, self.sharks)
        self.violets = list(filter(lambda violet: violet.alive, self.violets))
        for shark in self.sharks:
            shark.update(dt)
        self.stats.violet_q = len(self.violets)
        self.stats.shark_q = len(self.sharks)
        self.stats.update()
        self.draw()
