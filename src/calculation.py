import math
from PIL import Image
import statistics

BODY_W = 0.70
BODY_H = 0.40
HEAD_W = 0.20
HEAD_H = 0.60
'''
BODY_W = 0.0
BODY_H = 0.0
HEAD_W = 0.0
HEAD_H = 0.0
'''


def calculate_brightness_for_pixel(r, g, b):
    r = float(r)
    g = float(g)
    b = float(b)
    return math.sqrt(0.241*math.pow(r, 2.0) + 0.691*math.pow(r, 2.0) +
                     0.068*math.pow(b, 2.0))


def ponderate(value):
    if value >= 15:
        return (math.log10(value)-math.log10(10.0))*100.0
    return value


def calculate_brightness_for_image(image):
    im = Image.open(image)
    pix = im.load()
    width, height = im.size
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
                    r, g, b)/255.0*100.0)
                data.append(ponderate(brightness))
    '''
    mean()	Arithmetic mean (“average”) of data.
    median()	Median (middle value) of data.
    median_low()	Low median of data.
    median_high()	High median of data.
    median_grouped()	Median, or 50th percentile, of grouped data.
    mode() Mode (most common value) of discrete data.
    return (statistics.mean(data), statistics.median(data),
            statistics.median_low(data), statistics.median_high(data),
            statistics.median_grouped(data), statistics.mode(data),
            max(data), min(data))
    '''
    return int(statistics.mean(data))

if __name__ == '__main__':
    print(calculate_brightness_for_image(
        '/home/lorenzo/Imágenes/Webcam/2016-05-17-203726.jpg'))
    print(calculate_brightness_for_image(
        '/home/lorenzo/Imágenes/Webcam/2016-05-17-203831.jpg'))
    print(calculate_brightness_for_image(
        '/home/lorenzo/Imágenes/Webcam/2016-05-17-203853.jpg'))
    print(calculate_brightness_for_image(
        '/home/lorenzo/Imágenes/Webcam/2016-05-17-204238.jpg'))
