from PIL import Image
from pathlib import Path

import argparse

from common import *
from matrix import MatrixConstants


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

exif = dict(image._getexif().items())
orientation_id = 0x0112 # https://www.media.mit.edu/pia/Research/deepview/exif.html

if exif[orientation_id] == 3:
    image=image.rotate(180, expand=True)
elif exif[orientation_id] == 6:
    image=image.rotate(270, expand=True)
elif exif[orientation_id] == 8:
    image=image.rotate(90, expand=True)


width, height = image.size

width, height = int(100 * compression * args.width), int(height/(width/100) * compression)
image = image.resize((width, height))
image = image.convert('RGB')

m = MatrixConstants.HORIZONTAL

ascii_img = m.apply_on_image(image, func=diff)

# mini = 10e9
maxi = -10e9

for row in ascii_img:
    for pixel in row:
        # mini = min(pixel, mini)
        maxi = max(pixel, maxi)

output = ''

for row in ascii_img:
    for pixel in row:
        p = BRIGHTNESS[0]
        if pixel > 0:
            p = BRIGHTNESS[int((MAX_BRIGHTNESS - 1) * pixel/maxi)]
        output += p
    output += '\n'

if terminal_output: print(output)
else: f.write(output)
