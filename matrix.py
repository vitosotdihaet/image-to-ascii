from PIL import Image

from common import *


class Matrix:
    # TODO: add often edge detection constants

    def __init__(self, data):
        if len(data) % 2 != 1 or len(data) != len(data[0]):
            raise ValueError

        self.n = len(data)
        self.data = data

    def apply_on_image(self, img: Image.Image, func):
        width, height = img.size
        out = [[0. for _ in range(width)] for _ in range(height)]

        half = self.n // 2

        for y in range(half, height - half):
            for x in range(half, width - half):
                s = 0

                for dy in range(-half, half + 1):
                    for dx in range(-half, half + 1):
                        s += func(img.getpixel((x + dx, y + dy))) * self.data[half + dy][half + dx]

                out[y][x] = s / 9

        # TODO: set first and last half pixels from each side
        return out
    
    def __add__(self, other):
        if self.n != other.n:
            raise ValueError

        for y in range(self.n):
            for x in range(self.n):
                self.data[y][x] += other.data[y][x]
