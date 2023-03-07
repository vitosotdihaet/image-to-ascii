from PIL import Image
from pathlib import Path
from time import time

import argparse

DEFAULT_COMPRESSION = 0.5
# offset x for saving resolution
DEFAULT_RATIO = 2.35

parser = argparse.ArgumentParser()

parser.add_argument("path")
parser.add_argument("-c", "--compression", default=DEFAULT_COMPRESSION, type=float)
parser.add_argument("-s", "--save", action="store_true")
parser.add_argument("-b", "--inverse", action="store_true")
parser.add_argument("-w", "--width", default=DEFAULT_RATIO, type=float)

args = parser.parse_args()

target_img = Path(args.path)

if not target_img.is_file():
    print("The target image doesn't exist!")
    exit(1)

# inverse_brightness = True if terminal background is a bright color
inverse_brightness = args.inverse

# terminal_output = True if you want to print the result to terminal
terminal_output = not args.save

compression = args.compression

if not terminal_output: f = open(target_img.name[:-4] + '.txt', 'w')

brightness = '8@#DZL]waxv?1(/|=+*":_-,.`  '[::-1]
if inverse_brightness:
    brightness = brightness[::-1]

l = len(brightness)

image = Image.open(target_img)
x, y = image.size

x, y = int(100 * compression * args.width), int(y/(x/100) * compression)

image = image.resize((x, y))

pixels = image.convert('RGB')

for r in range(y):
    for c in range(x):
        colors = pixels.getpixel((c, r))
        gray = int(colors[0] * 0.3 + colors[1] * 0.5 + colors[2] * 0.2)

        cp = brightness[int(l * (gray - 1)/256)]

        if terminal_output: print(cp, end='')
        else: f.write(cp)

    if terminal_output: print()
    else: f.write('\n')

if not terminal_output: f.close()
