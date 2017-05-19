import math
import statistics
from PIL import Image

BODY_W = 0.70
BODY_H = 0.40
HEAD_W = 0.20
HEAD_H = 0.60


def calculate_brightness_for_pixel(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    return math.sqrt(0.241 * math.pow(r, 2.0) + 0.691 * math.pow(r, 2.0) +
                     0.068 * math.pow(b, 2.0))


def ponderate(value):
    if value >= 15:
        return (math.log10(value) - math.log10(10.0)) * 100.0
    return value


def calculate_brightness_for_file(image):
    im = Image.open(image)
    return calculate_brightness_for_image(im)


def calculate_brightness_for_image(image):
    pix = image.load()
    width, height = image.size
    width = float(width)
    height = float(height)
    data = []
    for y in range(0, int(height)):
        for x in range(0, int(width)):
            if (y < (1.0 - BODY_H - HEAD_H) * height) or\
                (y > (1.0 - BODY_H - HEAD_H) * height and
                 y < (1.0 - HEAD_H) * height and
                    (x < (1.0 - HEAD_W) / 2.0 * width or
                     x > (1.0 + HEAD_W) / 2.0)) or\
                (y > (1.0 - BODY_H) * height and
                    (x < (1.0 - BODY_W) / 2.0 * width or
                     x > (1.0 + BODY_W) / 2.0 * width)):
                r, g, b = pix[x, y]
                brightness = int(calculate_brightness_for_pixel(
                    r, g, b) / 255.0 * 100.0)
                data.append(ponderate(brightness))
    return int(statistics.mean(data))


if __name__ == '__main__':
    import os
    from comun import TESTDIR
    print('blanco',
          calculate_brightness_for_file(os.path.join(TESTDIR,
                                                     'test01-blanco.jpg')))
    print('negro',
          calculate_brightness_for_file(os.path.join(TESTDIR,
                                                     'test02-negro.jpg')))
    print('gris',
          calculate_brightness_for_file(os.path.join(TESTDIR,
                                                     'test03-gris.jpg')))
    print('naranja',
          calculate_brightness_for_file(os.path.join(TESTDIR,
                                                     'test04-naranja.jpg')))
