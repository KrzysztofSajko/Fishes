import pyglet
import random
from graphics.mainWindow import MainWindow


random.seed()
window = MainWindow()
fps = 120


def update(dt):
    window.update(dt)


pyglet.clock.schedule_interval(update, 1/fps)


if __name__ == '__main__':
    pyglet.app.run()
