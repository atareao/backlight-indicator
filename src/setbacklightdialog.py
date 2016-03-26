#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# setbacklightdialog.py
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

from gi.repository import Gtk
import comun
from configurator import Configuration
from comun import _
from backlight import BacklightManager


class SetBacklightDialog(Gtk.Dialog):
    def __init__(self):
        #
        Gtk.Dialog.__init__(self,
                            'Backlight Indicator | '+_('Set backlight'),
                            None,
                            Gtk.DialogFlags.MODAL |
                            Gtk.DialogFlags.DESTROY_WITH_PARENT,
                            (Gtk.STOCK_CANCEL, Gtk.ResponseType.REJECT,
                                Gtk.STOCK_OK, Gtk.ResponseType.ACCEPT))
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        self.connect('close', self.close_ok)
        self.set_icon_from_file(comun.ICON)
        #
        vbox0 = Gtk.VBox(spacing=5)
        vbox0.set_border_width(5)
        self.get_content_area().add(vbox0)
        frame0 = Gtk.Frame()
        vbox0.pack_start(frame0, False, True, 1)
        table0 = Gtk.Table(2, 2, False)
        frame0.add(table0)
        label23 = Gtk.Label(_('Backlight')+':')
        label23.set_alignment(0, 0.5)
        table0.attach(label23, 0, 1, 0, 1,
                      xpadding=5, ypadding=5)
        configuration = Configuration()
        minimum_backlight = configuration.get('minimum-backlight')
        maximum_backlight = configuration.get('maximum-backlight')
        ba = BacklightManager()
        backlight = ba.get_backlight()
        adjustment3 = Gtk.Adjustment(backlight,
                                     minimum_backlight,
                                     maximum_backlight, 5, 10, 1)
        self.backlight = Gtk.Scale()
        self.backlight.set_digits(0)
        self.backlight.set_size_request(200, 10)
        self.backlight.set_adjustment(adjustment3)
        table0.attach(self.backlight, 1, 2, 0, 1,
                      xpadding=5, ypadding=5)
        self.show_all()

    def close_ok(self):
        self.hide()

    def get_selected_backlight(self):
        return int(self.backlight.get_value())

if __name__ == "__main__":
    cm = SetBacklightDialog()
    if cm.run() == Gtk.ResponseType.ACCEPT:
        print(cm.get_selected_backlight())
        cm.close_ok()
    cm.destroy()
    exit(0)
