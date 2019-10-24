import pyglet
import math
import utils
from random import randint, random
from myenum import MyEnum
from enum import auto


class FishStats(MyEnum):
    start_pop = auto()
    img_path = auto()
    img_scale = auto()
    eat_range = auto()
    max_vel_l = auto()
    vel_l_threshold = auto()
    max_acc_l = auto()
    min_d_acc_l = auto()
    max_d_acc_l = auto()
    prob_change_l = auto()
    max_vel_r = auto()
    vel_r_threshold = auto()
    max_acc_r = auto()
    min_d_acc_r = auto()
    max_d_acc_r = auto()
    prob_change_r = auto()


class Species(MyEnum):
    Shark = auto()
    Violet = auto()

    @property
    def stats(self):
        if self == self.Shark:
            return {FishStats.start_pop: 2, FishStats.eat_range: 0.8,
                    # image
                    FishStats.img_path: "sprites/shark_m.png", FishStats.img_scale: 0.2,
                    # linear movement
                    FishStats.max_vel_l: 50, FishStats.max_acc_l: 5, FishStats.prob_change_l: 0.3,
                    FishStats.min_d_acc_l: -2, FishStats.max_d_acc_l: 2,
                    FishStats.vel_l_threshold: 0.7,
                    # rotation movement
                    FishStats.max_vel_r: 50, FishStats.max_acc_r: 5, FishStats.prob_change_r: 0.3,
                    FishStats.min_d_acc_r: -2, FishStats.max_d_acc_r: 2,
                    FishStats.vel_r_threshold: 0.3}
        elif self == self.Violet:
            return {FishStats.start_pop: 100, FishStats.eat_range: 0.8,
                    # image
                    FishStats.img_path: "sprites/fish_1.png", FishStats.img_scale: 0.03,
                    # linear movement
                    FishStats.max_vel_l: 150, FishStats.max_acc_l: 50, FishStats.prob_change_l: 1,
                    FishStats.min_d_acc_l: -5, FishStats.max_d_acc_l: 5,
                    FishStats.vel_l_threshold: 0.7,
                    # rotation movement
                    FishStats.max_vel_r: 200, FishStats.max_acc_r: 50, FishStats.prob_change_r: 1,
                    FishStats.min_d_acc_r: -10, FishStats.max_d_acc_r: 10,
                    FishStats.vel_r_threshold: 0.3}


class Fish:
    def __init__(self, win_info, species, img):
        self.batch = win_info["batch"]
        self.group = win_info["group"]
        self.win_width = win_info["width"]
        self.win_height = win_info["height"]
        # position
        self.x = None
        self.y = None
        self.r = None
        self.dir = None
        # motion
        self.vel_l = 0
        self.acc_l = 0
        self.vel_r = 0
        self.acc_r = 0
        # status
        self.alive = True
        self.species = species
        # sprite
        self.sprite = None
        self.load(img)

    def load(self, img):
        # make sprite
        self.sprite = pyglet.sprite.Sprite(img, batch=self.batch, group=self.group)
        self.sprite.update(scale=self.species.stats[FishStats.img_scale])
        # set random position
        self.x = randint(self.sprite.width // 2, self.win_width - self.sprite.width // 2)
        self.y = randint(self.sprite.height // 2, self.win_height - self.sprite.height // 2)
        self.r = randint(0, 360)
        self.dir = self.r
        # set random velocity
        self.vel_l = self.species.stats[FishStats.max_vel_l]

    def move(self, dt):
        # check if acceleration changes
        # linear
        if random() < self.species.stats[FishStats.prob_change_l]:
            self.acc_l += randint(self.species.stats[FishStats.min_d_acc_l], self.species.stats[FishStats.max_d_acc_l])
            self.acc_l = utils.trim(self.acc_l, -self.species.stats[FishStats.max_acc_l],
                                    self.species.stats[FishStats.max_acc_l])
        # rotation
        if self.vel_r > self.species.stats[FishStats.vel_r_threshold] * self.species.stats[FishStats.max_vel_r]:
            vel_ratio = self.vel_r / self.species.stats[FishStats.max_vel_r]
            min_d_acc_r = (1 + vel_ratio) * self.species.stats[FishStats.min_d_acc_r]
            max_d_acc_r = (1 - vel_ratio) * self.species.stats[FishStats.max_d_acc_r]
        else:
            min_d_acc_r = self.species.stats[FishStats.min_d_acc_r]
            max_d_acc_r = self.species.stats[FishStats.max_d_acc_r]
        if random() < self.species.stats[FishStats.prob_change_r]:
            self.acc_r += randint(int(min_d_acc_r), int(max_d_acc_r))
            self.acc_r = utils.trim(self.acc_r, -self.species.stats[FishStats.max_acc_r],
                                    self.species.stats[FishStats.max_acc_r])
        # update velocities
        self.vel_l += self.acc_l * dt
        self.vel_l = utils.trim(self.vel_l, self.species.stats[FishStats.vel_l_threshold] * self.species.stats[FishStats.max_vel_l],
                                self.species.stats[FishStats.max_vel_l])
        self.vel_r += self.acc_r * dt
        self.vel_r = utils.trim(self.vel_r, -self.species.stats[FishStats.max_vel_r],
                                self.species.stats[FishStats.max_vel_r])
        # update position
        self.r += self.vel_r * dt
        self.dir = self.r
        rad = math.radians(self.dir)
        self.x += self.vel_l * dt * math.cos(rad)
        self.y -= self.vel_l * dt * math.sin(rad)

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
    img = pyglet.image.load(Species.Shark.stats[FishStats.img_path])
    utils.center_img(img)
    size = (img.width + img.height) * Species.Shark.stats[FishStats.img_scale] / 4

    def __init__(self, win_info):
        super().__init__(win_info=win_info, species=Species.Shark, img=Shark.img)


class Violet(Fish):
    img = pyglet.image.load(Species.Violet.stats[FishStats.img_path])
    utils.center_img(img)
    size = (img.width + img.height) * Species.Violet.stats[FishStats.img_scale] / 4

    def __init__(self, win_info):
        super().__init__(win_info=win_info, species=Species.Violet, img=Violet.img)

    def check_shark(self, sharks):
        if not isinstance(sharks, list):
            print("Sharks param is not a list")
            exit(1)
        for shark in sharks:
            dist = utils.distance(self.x, self.y, shark.x, shark.y)
            if dist - self.size < shark.size * shark.species.stats[FishStats.eat_range]:
                self.alive = False
                break

    def update(self, dt, sharks):
        super().update(dt)
        self.check_shark(sharks)

