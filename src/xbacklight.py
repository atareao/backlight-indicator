#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# xbacklight.py
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

import subprocess
import shlex


def execute(command):
    commandandargs = shlex.split(command)
    return subprocess.check_output(commandandargs, universal_newlines=True)


class BacklightManager():

    def __init__(self):
        self.backlight = 0
        self.update_backlight()

    def get_backlight(self):
        self.update_backlight()
        return self.backlight

    def update_backlight(self):
        self.backlight = float(execute('xbacklight -get'))

    def set_backlight(self, value):
        execute('xbacklight -set %s' % (value))
        self.update_backlight()

if __name__ == '__main__':
    bm = BacklightManager()
    print(bm.get_backlight())
    bm.set_backlight(50)
    print(bm.get_backlight())
    from webcam import Webcam
    wc = Webcam()
    b = wc.get_brightness()
    print(b)
    bm.set_backlight(b)
