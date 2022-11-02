from PIL import Image
import os

if not os.path.exists('i.jpg'):
    print(f'i.jpg does not exist in {os.getcwd()}!')
    print(f'Please check file\'s extension!')
    exit()

f = open('o.txt', 'w')

# inverse = True if terminal background is a bright color
inverse = False

# terminal_output = True if you want to print the result to terminal
terminal_output = False

brightness = '8@#DZL]waxv?1(/|=+*":_-,.`  '[::-1]
if inverse:
    brightness = brightness[::-1]

l = len(brightness)
compression = 0.5

image = Image.open('i.jpg')
x, y = image.size

# offset x for saving resolution
x, y = int(100 * compression * 2.35), int(y/(x/100) * compression)

image = image.resize((x, y))

pixels = image.convert('RGB')

for r in range(y):
    for c in range(x):
        colors = pixels.getpixel((c, r))
        gray = int(colors[0] * 0.3 + colors[1] * 0.5 + colors[2] * 0.2)
        cp = brightness[int(l * (gray - 1)/256)]
        f.write(cp)
        if terminal_output:
            print(cp, end='')
    f.write('\n')
    if terminal_output:
        print()

f.close()
