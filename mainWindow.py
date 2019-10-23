import pyglet
import math
from graphics.fish import Violet, Shark


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__(width=1280, height=720, caption="Woobly fishes wooblying")
        pyglet.gl.glClearColor(0.06, 0.06, 0.06, 1)
        self.set_location(120, 60)
        self.elements = []
        self.batch = pyglet.graphics.Batch()
        self.violet_q = 1000
        self.shark_q = 10
        self.background = None
        self.setup()

    def setup(self):
        # load background
        bg = pyglet.image.load("sprites/underwater_bcg.png")
        self.background = pyglet.sprite.Sprite(bg, 0, 0)
        self.background.scale_x = self.width / bg.width
        self.background.scale_y = self.height / bg.height
        # create violets
        for i in range(self.violet_q):
            self.elements.append(Violet(self.batch, self.width, self.height))
        # create violets
        for i in range(self.shark_q):
            self.elements.append(Shark(self.batch, self.width, self.height))

    def draw(self):
        self.clear()
        self.background.draw()
        self.batch.draw()

    def update(self, dt):
        for el in self.elements:
            el.update(dt)
        self.draw()
