#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of 2gif
#
# Copyright (C) 2015-2016 Lorenzo Carbonell
# lorenzo.carbonell.cerezo@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
try:
    gi.require_version('GdkPixbuf', '2.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import GdkPixbuf
from PIL import Image
import calculation
import subprocess
import shlex

COMMAND = 'fswebcam -r 640x480 --jpeg 100 --no-banner -S 10 /tmp/fswebcam.jpg'


class Webcam():
    ''' Sets up a pipe from the camera to a pixbuf and emits a signal
    when the image is ready. '''

    def __init__(self):
        ''' Prepare camera pipeline to pixbuf and signal watch '''
        pass

    def get_backlight(self):

        subprocess.call(shlex.split(COMMAND))
        pixbuf = GdkPixbuf.Pixbuf.new_from_file('/tmp/fswebcam.jpg')
        image = Image.frombytes('RGB',
                                (pixbuf.get_width(),
                                 pixbuf.get_height()),
                                pixbuf.get_pixels())
        pixbuf.savev('/home/lorenzo/Escritorio/test.png', "png", [], [])
        return calculation.calculate_brightness_for_image(image)


if __name__ == '__main__':
    webcam = Webcam()
    print('---', webcam.get_backlight(), '---')
