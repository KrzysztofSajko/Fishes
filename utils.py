import math


def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx*dx + dy*dy)


def center_img(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2


def trim(val, lower_boundary, upper_boundary):
    if val < lower_boundary:
        val = lower_boundary
    elif val > upper_boundary:
        val = upper_boundary
    return val
