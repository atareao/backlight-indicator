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
import os

DBUS_PROPS = {
    'ubuntu': {
        "service": "org.gnome.SettingsDaemon",
        "path": "/org/gnome/SettingsDaemon/Power",
        "interface": "org.gnome.SettingsDaemon.Power.Screen",
        "method-set": "SetPercentage",
        "method-get": "GetPercentage"
    },
    'gnome': {
        "service": "org.gnome.SettingsDaemon",
        "path": "/org/gnome/SettingsDaemon/Power",
        "interface": "org.gnome.SettingsDaemon.Power.Screen",
        "method-set": "SetPercentage",
        "method-get": "GetPercentage"
    },
    'mate': {
        "service": "org.mate.PowerManager",
        "path": "/org/mate/PowerManager/Backlight",
        "interface": "org.mate.PowerManager.Backlight",
        "method-set": "SetBrightness",
        "method-get": "GetBrightness"
    },
    'kde': {
        "service": "org.kde.Solid.PowerManagement",
        "path": "/org/kde/Solid/PowerManagement/Actions/BrightnessControl",
        "interface": "org.kde.Solid.PowerManagement.Actions.BrightnessControl",
        "method-set": "setBrightness",
        "method-get": "brightness"
    }
}


class BacklightManager:
    def __init__(self):
        self.desktop = os.getenv('DESKTOP_SESSION', 'gnome')
        properties = DBUS_PROPS[self.desktop]
        self.callback = None
        self.bus = dbus.SessionBus()
        bus = dbus.SessionBus()
        proxy = bus.get_object(properties['service'], properties['path'])
        self.properties_manager = dbus.Interface(
            proxy, 'org.freedesktop.DBus.Properties')
        self.dbus_interface = dbus.Interface(
            proxy, dbus_interface=properties['interface'])
        self.get_value = self.dbus_interface.get_dbus_method(
            properties['method-get'])
        self.set_value = self.dbus_interface.get_dbus_method(
            properties['method-set'])
        self.callback = None

    def get_backlight(self):
        if self.desktop == 'gnome':
            curr_value = self.properties_manager.Get(
                'org.gnome.SettingsDaemon.Power.Screen', 'Brightness')
            return int(curr_value)
        return int(self.get_value())

    def set_backlight(self, value):
        if self.desktop == 'gnome':
            curr_value = self.properties_manager.Set(
                'org.gnome.SettingsDaemon.Power.Screen',
                'Brightness',
                value)
        else:
            self.set_value(value)

    def set_callback(self, callback):
        self.callback = callback

    def backlight_changed(self, changed_value):
        if self.callback:
            self.callback(changed_value)


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
