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

import gi
try:
    gi.require_version('Gst', '1.0')
except Exception as e:
    print(e)
    exit(1)
from gi.repository import Gst
from PIL import Image
from PIL import ImageStat
import os
import time
import tempfile
import math

Gst.init(None)


class Webcam:
    def __init__(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            prefix='tmp_calculate_backlight_').name + '.jpg'
        self.pipeline = Gst.Pipeline()
        src = Gst.ElementFactory.make('v4l2src', '/dev/video0')
        filter1 = Gst.ElementFactory.make('videoconvert', None)
        filter2 = Gst.ElementFactory.make('videoscale', None)
        filter3 = Gst.ElementFactory.make('videorate', None)
        caps = Gst.Caps.from_string('video/x-raw, framerate=1/1')
        camerafilter = Gst.ElementFactory.make("capsfilter", "capsfilter")
        camerafilter.set_property('caps', caps)
        filter4 = Gst.ElementFactory.make('jpegenc', None)
        filter5 = Gst.ElementFactory.make('multifilesink', None)
        # filter5.set_property('location', 'test%010d.jpg')
        filter5.set_property('location', self.temp_file)
        self.pipeline.add(src)
        self.pipeline.add(filter1)
        self.pipeline.add(filter2)
        self.pipeline.add(filter3)
        self.pipeline.add(camerafilter)
        self.pipeline.add(filter4)
        self.pipeline.add(filter5)
        src.link(filter1)
        filter1.link(filter2)
        filter2.link(filter3)
        filter3.link(camerafilter)
        camerafilter.link(filter4)
        filter4.link(filter5)

    def get_backlight(self):
        self.pipeline.set_state(Gst.State.PLAYING)
        time.sleep(5)
        self.pipeline.set_state(Gst.State.NULL)
        # im = Image.open(self.temp_file).convert('L')
        im = Image.open(self.temp_file).convert('L')
        stat = ImageStat.Stat(im)
        '''
        print('extrema', stat.extrema)
        print('mean', stat.mean)
        print('median', stat.median)
        print('rms', stat.rms)
        print('var', stat.var)
        print('stddev', stat.stddev)
        print(im.histogram())
        '''
        if os.path.exists(self.temp_file):
            # os.remove(self.temp_file)
            pass
        value = int(stat.extrema[0][1]/255.0*100)
        return value


if __name__ == '__main__':
    webcam = Webcam()
    print(webcam.get_backlight())
