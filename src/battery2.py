#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# battery.py
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

import os


class Battery():

    @staticmethod
    def __get(variable):
        afile = open('/sys/class/power_supply/BAT0/{}'.format(variable),
                     'r')
        value = afile.read().strip()
        afile.close()
        return value

    @staticmethod
    def with_battery():
        return os.path.exists('/sys/class/power_supply/BAT0')

    @staticmethod
    def is_charging():
        if not Battery.with_battery():
            return False
        value = Battery.__get('status')
        if value == 'Charging':
            return True
        elif value == 'Discharging':
            return False
        elif value == 'Full':
            return False
        else:
            return False

    @staticmethod
    def is_ac():
        if not Battery.with_battery():
            return True
        value = Battery.__get('status')
        if value == 'Charging':
            return True
        elif value == 'Discharging':
            return False
        elif value == 'Full':
            return True
        else:
            return False

    @staticmethod
    def get_percentage():
        if not Battery.with_battery():
            return -1
        return int(Battery.__get('capacity'))

    @staticmethod
    def get_current_now():
        if not Battery.with_battery():
            return -1
        return int(Battery.__get('current_now'))

    @staticmethod
    def get_charge_now():
        if not Battery.with_battery():
            return -1
        return int(Battery.__get('charge_now'))

    @staticmethod
    def get_charge_full():
        if not Battery.with_battery():
            return -1
        return int(Battery.__get('charge_full'))

    @staticmethod
    def get_lifetime():
        if not Battery.with_battery():
            return -1
        full_capacity = Battery.get_charge_full()
        remaining = Battery.get_charge_now()
        drain_rate = Battery.get_current_now()
        if Battery.is_charging():
            return (full_capacity - remaining) / drain_rate * 60
        elif drain_rate > 0:
            return remaining / drain_rate * 60
        return -1

if __name__ == '__main__':
    print(Battery.with_battery())
    print(Battery.is_charging())
    print(Battery.is_ac())
    print(Battery.get_percentage())
    print(Battery.get_current_now())
    print(Battery.get_charge_now())
    print(Battery.get_charge_full())
    print(Battery.get_lifetime())
