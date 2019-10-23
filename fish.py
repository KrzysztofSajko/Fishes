import pyglet
import math
from random import randint


class Fish:
    def __init__(self, batch, win_width, win_height, v, img, scale):
        self.sprite = None
        self.batch = batch
        self.win_width = win_width
        self.win_height = win_height
        self.x = None
        self.y = None
        self.r = None
        self.dir = None
        self.v = v
        self.scale = scale
        self.load(img)

    def load(self, img):
        # make sprite
        self.sprite = pyglet.sprite.Sprite(img, batch=self.batch)
        self.sprite.update(scale=self.scale)
        # set random coords
        self.x = randint(self.sprite.width // 2, self.win_width - self.sprite.width // 2)
        self.y = randint(self.sprite.height // 2, self.win_height - self.sprite.height // 2)
        self.r = randint(0, 360)
        self.dir = self.r

    def move(self, dt):
        rad = math.radians(self.dir)
        self.x += self.v * dt * math.cos(rad)
        self.y -= self.v * dt * math.sin(rad)

    def check_collision(self):
        rotation_offset = None
        height = self.sprite.height // 2
        width = self.sprite.width // 2
        # check vertical walls
        if self.x < width:
            self.x = width
            rotation_offset = 520
        elif self.x > self.win_width - width:
            self.x = self.win_width - width
            rotation_offset = 520
        # check horizontal walls
        if self.y < height:
            self.y = height
            rotation_offset = 360
        elif self.y > self.win_height - height:
            self.y = self.win_height - height
            rotation_offset = 360
        # change direction if collision detected
        if rotation_offset:
            self.r = rotation_offset - self.r
            self.dir = rotation_offset - self.dir

    def update(self, dt):
        self.move(dt)
        self.check_collision()
        self.sprite.update(x=self.x, y=self.y, rotation=self.r)

    def draw(self):
        self.sprite.draw()


class Shark(Fish):
    img = pyglet.image.load("sprites/shark_m.png")
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    scale = 0.2

    def __init__(self, batch, win_width, win_height):
        super().__init__(batch, win_width, win_height, v=200, img=Shark.img, scale=Shark.scale)


class Violet(Fish):
    img = pyglet.image.load("sprites/fish_1.png")
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2
    scale = 0.05

    def __init__(self, batch, win_width, win_height):
        super().__init__(batch, win_width, win_height, v=200, img=Violet.img, scale=Violet.scale)
