#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# backlight.py
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
import dbus

DBUS_INTERFACE = "org.gnome.SettingsDaemon.Power.Screen"


class BacklightManager:
    def __init__(self):
        self.callback = None
        self.bus = dbus.SessionBus()
        bus = dbus.SessionBus()
        proxy = bus.get_object("org.gnome.SettingsDaemon",
                               "/org/gnome/SettingsDaemon/Power")
        self.dbus_interface = dbus.Interface(proxy,
                                             dbus_interface=DBUS_INTERFACE)
        # self.dbus_interface.connect_to_signal("PercentageChanged",
        #                                      self.backlight_changed)

        self.callback = None

    def get_backlight(self):
        return int(self.dbus_interface.GetPercentage())

    def set_backlight(self, value):
        self.dbus_interface.SetPercentage(value)

    def set_callback(self, callback):
        self.callback = callback

    def backlight_changed(self, changed_value):
        if self.callback:
            self.callback(changed_value)
            print(self.get_value())


def sample(changed_value):
    print('Example', changed_value)

if __name__ == '__main__':
    ba = BacklightManager()
    ba.set_callback(sample)
    print(ba.get_backlight())
    ba.set_backlight(40)
    print(ba.get_backlight())
    ba.set_backlight(30)
    print(ba.get_backlight())
    ba.set_backlight(20)
    print(ba.get_backlight())
    ba.set_backlight(30)
    print(ba.get_backlight())
    ba.set_backlight(50)
    print(ba.get_backlight())
