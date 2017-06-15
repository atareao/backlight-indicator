#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# webcam.py
#
# This file is part of Backlight Indicator
#
# Copyright (C) 2016
# Lorenzo Carbonell Cerezo <lorenzo.carbonell.cerezo@gmail.com>
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

from PIL import Image
import time
import calculation
import select
import v4l2capture

DEVICES = ['/dev/video0', '/dev/video1', '/dev/video2']


class Webcam:
    def __init__(self):
        pass

    def get_backlight():
        image_data = None
        try:
            video = v4l2capture.Video_device('/dev/video0')
            size_x, size_y = video.set_format(1280, 1024)
            video.create_buffers(1)
            video.start()
            time.sleep(2)
            video.queue_all_buffers()
            select.select((video,), (), ())
            image_data = video.read()
        except Exception as e:
            print('-----', e, '-----')
        finally:
            video.stop()
            video.close()
        if image_data is not None:
            image = Image.frombytes("RGB",
                                    (size_x, size_y),
                                    image_data)
            value = calculation.calculate_brightness_for_image(image)
            print('==== captured: {0} ===='.format(value))
            return value
        return None


if __name__ == '__main__':
    webcam = Webcam()
    print(Webcam.get_backlight())
