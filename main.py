from PIL import Image
from pathlib import Path

import argparse

import pixel_to_value
import matrix


DEFAULT_COMPRESSION = 0.5
DEFAULT_WIDTH_RATIO = 2.35
DEFAULT_PIXEL_TO_VALUE_FUNCTION = 'diff'
DEFAULT_EDGE_FUNCTION = 'unweighted'

BRIGHTNESS = '8@#DZL]waxv?1(/|=+*\':_-,.` '[::-1]
MAX_BRIGHTNESS = len(BRIGHTNESS)


def straighten_image(image: Image.Image):
    # https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Exif
    exif = image.getexif()
    orientation_id = 0x0112  # https://www.media.mit.edu/pia/Research/deepview/exif.html

    if orientation_id in exif:  # there is an orientation info in metadata
        # rotate an image
        if exif[orientation_id] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation_id] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation_id] == 8:
            image = image.rotate(90, expand=True)

# parse arguments


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('path', type=str, help='Path to an image file')
    parser.add_argument('-c', '--compression', default=DEFAULT_COMPRESSION, type=float,
                        help='Coefficient of a compression: if compression is 0.5, the resolution goes from 1920x1080 to 960x540')
    parser.add_argument('-i', '--inverse', action='store_true',
                        help='Inverse the brightness')
    parser.add_argument('-p', '--pixel_to_value_function', default=DEFAULT_PIXEL_TO_VALUE_FUNCTION,
                        type=str, help='A function to interpret colors as floats', choices=pixel_to_value.all.keys())
    parser.add_argument('-e', '--edge_detection_matrix', default=DEFAULT_EDGE_FUNCTION, type=str,
                        help='A matrix for edge detections', choices=matrix.MatrixConstants.all.keys())
    parser.add_argument('-w', '--width', default=DEFAULT_WIDTH_RATIO, type=float,
                        help='Ratio of width multiplication (reason is char\'s height is bigger than its width)')
    parser.add_argument('-s', '--save', action='store_true',
                        help='Save the output to a file <image_name>.txt')

    return parser.parse_args()


args = get_args()


# set variables to argument values
image_path = Path(args.path)
if not image_path.is_file():
    print('The target image doesn\'t exist!')
    exit(1)

compression = args.compression
terminal_output = not args.save

if args.inverse:
    BRIGHTNESS = BRIGHTNESS[::-1]

pixel_to_value_function = pixel_to_value.all[args.pixel_to_value_function]
edge_detection_matrix = matrix.MatrixConstants.all[args.edge_detection_matrix]

if not terminal_output:
    f = open(image_path.stem + '.txt', 'w')


image = Image.open(image_path)
straighten_image(image)


width, height = image.size
ratio = height / width

# output width and height
width = int(args.width * 100 * compression)
height = int(ratio * 100 * compression)

image = image.resize((width, height))
image = image.convert('RGB')


matrix_applied_image = edge_detection_matrix.apply_on_image(
    image, func=pixel_to_value_function)


# get max value to set up brightness
maxi = 0
for row in matrix_applied_image:
    for pixel in row:
        maxi = max(pixel, maxi)

# map pixel values to ascii
ascii_representation = ''
for row in matrix_applied_image:
    for pixel in row:
        p = BRIGHTNESS[int((MAX_BRIGHTNESS - 1) * pixel / maxi)]
        ascii_representation += p
    ascii_representation += '\n'


if terminal_output:
    print(ascii_representation)
else:
    f.write(ascii_representation)
