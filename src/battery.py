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
import dbus
from enum import Enum
from gi.repository import GObject

# https://upower.freedesktop.org/docs/Device.html

DBUS_PROPS = {
    "service": "org.freedesktop.UPower",
    "path": "/org/freedesktop/UPower/devices/battery_BAT0",
    "interface": "org.freedesktop.DBus.Properties",
    "method-info": "org.freedesktop.UPower.Device"
}
DBUS_PROPS0 = {
    "service": "org.freedesktop.UPower",
    "path": "/org/freedesktop/UPower",
    "interface": "org.freedesktop.UPower",
    "method-info": "org.freedesktop.UPower.Device"
}


class State(Enum):
    unknown = 0
    charging = 1
    discharging = 2
    empty = 3
    fully_charged = 4
    pending_cherge = 5
    pending_discharge = 6


class Type(Enum):
    unknown = 0
    line_power = 1
    battery = 2
    ups = 3
    monitor = 4
    mouse = 5
    keyboard = 6
    pda = 6
    phone = 6


class Devices:
    def __init__(self):
        bus = dbus.SystemBus()
        proxy = bus.get_object(DBUS_PROPS0['service'], DBUS_PROPS0['path'])
        self.iface = dbus.Interface(
            proxy, dbus_interface=DBUS_PROPS0['interface'])

    def get_devices(self):
        return self.iface.EnumerateDevices()


class Battery:
    def __init__(self):
        bus = dbus.SystemBus()
        proxy = bus.get_object(DBUS_PROPS['service'], DBUS_PROPS['path'])
        self.iface = dbus.Interface(
            proxy, dbus_interface=DBUS_PROPS['interface'])

    def __get(self, variable):
        return self.iface.Get(DBUS_PROPS['method-info'], variable)

    def get_percentage(self):
        """
        The amount of energy left in the power source expressed as a percentage
        between 0 and 100. Typically this is the same as (energy -
        energy-empty) / (energy-full - energy-empty). However, some primitive
        power sources are capable of only reporting percentages and in this
        case the energy-* properties will be unset while this property is set.
        """
        return float(self.__get('Percentage'))

    def get_capacity(self):
        """
        The capacity of the power source expressed as a percentage between 0
        and 100. The capacity of the battery will reduce with age. A capacity
        value less than 75% is usually a sign that you should renew your
        battery. Typically this value is the same as
        (full-design / full) * 100. However, some primitive power sources are
        not capable reporting capacity and in this case the capacity property
        will be unset.
        """
        return float(self.__get('Capacity'))

    def get_state(self):
        """
        The battery power state.
        """
        return State(int(self.__get('State')))

    def is_charging(self):
        return self.get_state() == State.charging

    def is_rechargeable(self):
        """
        If the power source is rechargeable.
        """
        return bool(self.__get('IsRechargeable'))

    def get_native_path(self):
        return self.__get('NativePath')

    def get_vendor(self):
        return self.__get('Vendor')

    def get_model(self):
        return self.__get('Model')

    def get_serial(self):
        return self.__get('Serial')

    def get_type(self):
        return Type(int(self.__get('Type')))

    def is_online(self):
        """
        Whether power is currently being provided through line power. This
        property is only valid if the property type has the value "line-power".
        """
        return bool(self.__get('Online'))

    def get_energy(self):
        """
        Amount of energy (measured in Wh) currently available in the power
        source.
        """
        return float(self.__get('Energy'))

    def get_energy_empty(self):
        """
        Amount of energy (measured in Wh) in the power source when it's
        considered to be empty.
        """
        return float(self.__get('EnergyEmpty'))

    def get_energy_full(self):
        """
        Amount of energy (measured in Wh) in the power source when it's
        considered full.
        """
        return float(self.__get('EnergyFull'))

    def get_energy_full_design(self):
        """
        Amount of energy (measured in Wh) the power source is designed to hold
        when it's considered full.
        """
        return float(self.__get('EnergyFullDesign'))

    def get_energy_rate(self):
        """
        Amount of energy being drained from the source, measured in W. If
        positive, the source is being discharged, if negative it's being
        charged.
        """
        return float(self.__get('EnergyRate'))

    def get_voltage(self):
        """
        Voltage in the Cell or being recorded by the meter.
        """
        return float(self.__get('Voltage'))

    def get_time_to_empty(self):
        """
        Number of seconds until the power source is considered empty. Is set to
        0 if unknown.
        """
        return self.__get('TimeToEmpty')

    def get_time_to_full(self):
        """
        Number of seconds until the power source is considered full. Is set to
        0 if unknown.
        """
        return self.__get('TimeToEmpty')

    def is_ac(self):
        state = self.get_state()
        if state == State.charging or state == State.fully_charged:
            return True
        return False

    def is_present(self):
        """
        If the power source is present in the bay. This field is required as
        some batteries are hot-removable, for example expensive UPS and most
        laptop batteries.
        """
        return bool(self.__get('IsPresent'))

if __name__ == '__main__':
    bat = Battery()
    print(bat.get_percentage())
    print(bat.get_state())
    print(bat.is_charging())
    print(bat.is_rechargeable())
    print(bat.get_native_path())
    print(bat.get_vendor())
    print(bat.get_model())
    print(bat.get_serial())
    print(bat.get_type())
    print(bat.is_online())
    print(bat.get_energy())
    print(bat.get_energy_empty())
    print(bat.get_energy_full())
    print(bat.get_energy_full_design())
    print(bat.get_energy_rate())
    print(bat.get_voltage())
    print(bat.get_time_to_empty())
    print(bat.get_time_to_full())
    print(bat.is_ac())
    print(bat.is_present())
    print(bat.get_capacity())
