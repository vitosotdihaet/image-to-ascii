from PIL import Image

brightness = '8@#DZL]waxv?1(/|=+*":_-,.`  '[::-1]
l = len(brightness)
compress = 0.5

image = Image.open('image.jpg')
x, y = image.size

x, y = int(100 * compress * 2.35), int(y/(x/100) * compress)

image = image.resize((x, y))

pixels = image.convert('RGB')

for r in range(y):
    for c in range(x):
        colors = pixels.getpixel((c, r))
        gray = int(colors[0] * 0.3 + colors[1] * 0.5 + colors[2] * 0.2)
        print(brightness[int(l * (gray - 1)/256)], end='')
    print()