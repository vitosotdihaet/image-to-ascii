from PIL import Image

from common import *

from copy import copy


class Matrix:
    def __init__(self, data):
        if len(data) % 2 != 1 or len(data) != len(data[0]):
            raise ValueError

        self.n = len(data)
        self.data = data
    
    def default(self):
        self.n = 0
        self.data = []

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

                out[y][x] = max(0, s / 9)

        return out

    def __add__(self, other):
        if self.n != other.n:
            raise ValueError

        for y in range(self.n):
            for x in range(self.n):
                self.data[y][x] += other.data[y][x]

    def __mul__(self, coef: float | int):
        new = copy(self)

        for y in range(self.n):
            for x in range(self.n):
                new.data[y][x] *= coef

        return new
    
    def __copy__(self):
        return Matrix([[self.data[y][x] for x in range(self.n)] for y in range(self.n)])
    
    def __str__(self):
        s = ''

        for y in range(self.n):
            for x in range(self.n):
                s += f'{self.data[y][x]} '
            s += '\n'

        return s


class MatrixConstants:
    UNWEIGHTED = Matrix([[1]])

    HORIZONTAL = Matrix([
        [ 0, 0, 0],
        [-1, 0, 1],
        [ 0, 0, 0]
    ])

    VERTICAL = Matrix([
        [0, -1, 0],
        [0,  0, 0],
        [0,  1, 0],
    ])

    GAUSSIAN = Matrix([
        [-1, -2,  1],
        [-2,  0,  2],
        [-1,  2,  1]
    ])