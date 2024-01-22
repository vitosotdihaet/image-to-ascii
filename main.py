from PIL import Image
from pathlib import Path
from time import time

import argparse

from common import *
from matrix import *


DEFAULT_COMPRESSION = 0.5
DEFAULT_RATIO = 2.35

BRIGHTNESS = '8@#DZL]waxv?1(/|=+*":_-,.` '[::-1]
MAX_BRIGHTNESS = len(BRIGHTNESS)


# parse arguments
parser = argparse.ArgumentParser()

# path to an image file
parser.add_argument("path")
# coefficient of compression: example: if compression is 0.5, the resolution goes from 1920x1080 to 960x540
parser.add_argument("-c", "--compression", default=DEFAULT_COMPRESSION, type=float)
# save ascii version to a file <image_name>.txt
parser.add_argument("-s", "--save", action="store_true")
# inverse BRIGHTNESS of symbols
parser.add_argument("-b", "--inverse", action="store_true")
# coefficient of pixel width
parser.add_argument("-w", "--width", default=DEFAULT_RATIO, type=float)

args = parser.parse_args()


# set variables to argument values
target_img = Path(args.path)
if not target_img.is_file():
    print("The target image doesn't exist!")
    exit(1)

compression = args.compression
terminal_output = not args.save
if args.inverse: BRIGHTNESS = BRIGHTNESS[::-1]
if not terminal_output: f = open(target_img.name[:-4] + '.txt', 'w')


image = Image.open(target_img)
width, height = image.size

width, height = int(100 * compression * args.width), int(height/(width/100) * compression)
image = image.resize((width, height))
image = image.convert('RGB')

m = Matrix([
    [-1, -2,  1],
    [-2,  0,  2],
    [-1,  2,  1]
])

# m = Matrix([
#     [   0, 0,   0],
#     [-0.5, 0, 0.5],
#     [   0, 0,   0]
# ])

out = m.apply_on_image(image, func=grayscale)

# mini = 10e9
maxi = -10e9

for row in out:
    for pixel in row:
        # mini = min(pixel, mini)
        maxi = max(pixel, maxi)

for row in out:
    for pixel in row:
        p = BRIGHTNESS[0]
        if pixel > 0: p = BRIGHTNESS[int((MAX_BRIGHTNESS - 1) * pixel/maxi)]

        if terminal_output:
            print(p, end='')
        else:
            f.write(p)

    if terminal_output: print()
    else: f.write('\n')
