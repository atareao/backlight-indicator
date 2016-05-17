import math
from PIL import Image
from statistics import mode

BODY_W = 0.5
BODY_H = 0.25
HEAD_W = 0.25
HEAD_H = 0.25

def calculate_brightness_for_pixel(r, g, b):
    return math.sqrt(0.241*(r**2) + 0.691*(g**2) + 0.068*(b**2))

def calculate_brightness_for_image(image):
    im = Image.open(image)
    pix = im.load()
    width, height = im.size
    data = []
    for y in range (0, height):
        if y < (1 - BODY_H - HEAD_H) * height:
            for x in range(0, width):
                if (y > (1 - BODY_H - HEAD_H) * height and\
                        y < (1 - HEAD_H) * height and\
                        (x < (1 - HEAD_W) / 2 * width or\
                        x > (1 + HEAD_W) / 2)) or\
                        (y > (1 - BODY_H) * height and\
                        (x < (1 - BODY_W) / 2 * width or\
                        x > (1 + BODY_W) / 2 * width)):
                    r, g, b = pix[x, y]
                    brightness = int(calculate_brightness_for_pixel(r, g, b)/255)
                    data.append(brightness)
    return mode(data)

if __name__ == '__main__':
    print('echo')
