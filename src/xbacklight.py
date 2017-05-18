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

from acpilight import get_controllers, Controller


class BacklightManagerForGNOME():

    def __init__(self):
        ctrls = get_controllers()
        self.ctrl = Controller(next(iter(ctrls.values())))
        self.backlight = 0
        self.update_backlight()

    def get_backlight(self):
        self.update_backlight()
        return self.backlight

    def update_backlight(self):
        self.backlight = self.ctrl.brightness()

    def set_backlight(self, value):
        self.ctrl.set_brightness(value)
        self.update_backlight()


if __name__ == '__main__':
    bm = BacklightManagerForGNOME()
    print(bm.get_backlight())
    bm.set_backlight(50)
    print(bm.get_backlight())
    from webcam import Webcam
    wc = Webcam()
    b = wc.get_backlight()
    print(b)
    bm.set_backlight(b)
