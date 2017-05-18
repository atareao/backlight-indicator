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


class Webcam:
    def __init__(self):
        # Open the video device.
        self.video = v4l2capture.Video_device("/dev/video0")
        self.size_x, self.size_y = self.video.set_format(1280, 1024)

    def get_backlight(self):
        self.video.create_buffers(1)
        self.video.start()
        time.sleep(2)
        self.video.queue_all_buffers()
        select.select((self.video,), (), ())
        image_data = self.video.read()
        self.video.close()
        image = Image.frombytes("RGB", (self.size_x, self.size_y), image_data)
        value = calculation.calculate_brightness_for_image(image)
        return value


if __name__ == '__main__':
    webcam = Webcam()
    print(webcam.get_backlight())
