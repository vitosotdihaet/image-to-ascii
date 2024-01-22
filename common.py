def red(pixel):
    return pixel[0]

def green(pixel):
    return pixel[1]

def blue(pixel):
    return pixel[2]

def grayscale(pixel):
    return int(pixel[0] * 0.3 + pixel[1] * 0.5 + pixel[2] * 0.2)

def diff(pixel):
    return max(pixel) - min(pixel)