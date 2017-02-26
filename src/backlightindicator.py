#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# backlight-indicator.py
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
    gi.require_version('Gtk', '3.0')
    gi.require_version('AppIndicator3', '0.1')
    gi.require_version('Notify', '0.7')
    gi.require_version('Gst', '1.0')
except Exception as e:
    print(e)
    exit(-1)
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GdkPixbuf
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio
import time
import os
import webbrowser
import subprocess
import dbus
from configurator import Configuration
from preferences_dialog import PreferencesDialog
from setbacklightdialog import SetBacklightDialog
from comun import _
import comun
from webcam import Webcam
from backlight import BacklightManager
import threading
# from battery import Battery
from battery2 import Battery

gi.require_version('Gtk', '3.0')

WEBICON = os.path.join(comun.SOCIALDIR, 'web.svg')
TWITTERICON = os.path.join(comun.SOCIALDIR, 'twitter.svg')
GOOGLEPLUSICON = os.path.join(comun.SOCIALDIR, 'googleplus.svg')
FACEBOOKICON = os.path.join(comun.SOCIALDIR, 'facebook.svg')


def add2menu(menu, text=None, icon=None, conector_event=None,
             conector_action=None):
    if text is not None:
        menu_item = Gtk.ImageMenuItem.new_with_label(text)
        if icon:
            image = Gtk.Image.new_from_file(icon)
            menu_item.set_image(image)
            menu_item.set_always_show_image(True)
    else:
        if icon is None:
            menu_item = Gtk.SeparatorMenuItem()
        else:
            menu_item = Gtk.ImageMenuItem.new_from_file(icon)
            menu_item.set_always_show_image(True)
    if conector_event is not None and conector_action is not None:
        menu_item.connect(conector_event, conector_action)
    menu_item.show()
    menu.append(menu_item)
    return menu_item


class BacklightIndicator(GObject.GObject):
    __gsignals__ = {
        'session_end': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
        'break_end': (GObject.SIGNAL_RUN_FIRST, GObject.TYPE_NONE, ()),
    }

    def __init__(self):
        GObject.GObject.__init__(self)
        self.wid = 0
        # self.battery = Battery()
        self.webcam = Webcam()
        self.backlightManager = BacklightManager()
        self.icon = comun.ICON
        self.active_icon = None
        self.about_dialog = None
        self.active = False
        self.notification = Notify.Notification.new('', '', None)
        self.active_icon = comun.STATUS_ICON['light'][0]
        self._file = Gio.File.new_for_path(
            '/sys/class/power_supply/BAT0/status')
        self._monitor = Gio.File.monitor(self._file,
                                         Gio.FileMonitorFlags.NONE,
                                         None)
        self._monitor.connect("changed",
                              self._on_route_file_changed)
        #
        self.indicator = appindicator.Indicator.new(
            'BacklightIndicator', self.active_icon,
            appindicator.IndicatorCategory.HARDWARE)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.indicator.connect('scroll-event', self.on_scroll)
        menu = self.get_menu()
        self.indicator.set_menu(menu)
        self.read_preferences()
        # .connect('session_end', self.on_session_end)
        # self.connect('break_end', self.on_break_end)

    def on_scroll(self, widget, steps, direcction):
        if direcction == Gdk.ScrollDirection.UP:
            backlight = self.backlightManager.get_backlight()
            backlight += 10 * steps
            self.set_backlight(backlight)
            if self.show_value:
                self.indicator.set_label(str(int(self.backlight)), '')
            else:
                self.indicator.set_label('', '')
            if self.show_notifications:
                self.notification.update('Backlight-Indicator',
                                         _('Backlight')+': %s' % backlight,
                                         comun.STATUS_ICON[self.theme][0])
                self.notification.show()
        elif direcction == Gdk.ScrollDirection.DOWN:
            backlight = self.backlightManager.get_backlight()
            backlight -= 10 * steps
            self.set_backlight(backlight)
            if self.show_value:
                self.indicator.set_label(str(int(self.backlight)), '')
            else:
                self.indicator.set_label('', '')
            if self.show_notifications:
                self.notification.update('Backlight-Indicator',
                                         _('Backlight')+': %s' % backlight,
                                         comun.STATUS_ICON[self.theme][0])
                self.notification.show()

    # ################# main functions ####################
    def _on_route_file_changed(self, data):
        print('==== changed ====')

    def read_preferences(self):
        configuration = Configuration()
        self.first_time = configuration.get('first-time')
        self.version = configuration.get('version')
        self.autostart = configuration.get('autostart')
        self.theme = configuration.get('theme')
        self.show_notifications = configuration.get('show-notifications')
        self.show_value = configuration.get('show-value')
        self.minimum_backlight = configuration.get('minimum-backlight')
        self.maximum_backlight = configuration.get('maximum-backlight')
        self.backlight = configuration.get('backlight')
        self.sample_time = configuration.get('sample-time')
        self.autoworking = configuration.get('autoworking')
        self.change_on_ac = configuration.get('change-backlight-on-ac')
        self.value_on_ac = configuration.get('backlight-on-ac')
        self.change_on_low_power = configuration.get(
            'reduce-backlight-on-low-power')
        self.low_battery_value = configuration.get('low-battery-value')
        self.value_on_low_power = configuration.get('backlight-on-low-power')
        backlight = self.backlightManager.get_backlight()
        self.set_backlight(backlight)
        if self.show_value:
            self.indicator.set_label(str(int(self.backlight)), '')
        else:
            self.indicator.set_label('', '')
        if self.wid > 0:
            self.active_icon = comun.STATUS_ICON[self.theme][0]
            GLib.source_remove(self.wid)
            self.do_the_work()
            self.wid = GLib.timeout_add_seconds(self.sample_time * 60,
                                                self.do_the_work)
        else:
            if self.autoworking:
                self.start_automatically()
            else:
                self.active_icon = comun.STATUS_ICON[self.theme][1]

    def save_preferences(self):
        configuration = Configuration()
        configuration.set('backlight', self.backlight)
        configuration.save()

    # ################## menu creation ######################

    def get_help_menu(self):
        help_menu = Gtk.Menu()
        #
        add2menu(help_menu,
                 text=_('Homepage...'),
                 conector_event='activate',
                 conector_action=lambda x: webbrowser.open(
                     'https://launchpad.net/backlight-indicator'))
        add2menu(help_menu,
                 text=_('Get help online...'),
                 conector_event='activate',
                 conector_action=lambda x: webbrowser.open(
                     'https://answers.launchpad.net/backlight-indicator'))
        add2menu(help_menu,
                 text=_('Translate this application...'),
                 conector_event='activate',
                 conector_action=lambda x: webbrowser.open(
                     'https://translations.launchpad.net/backlight-indicator'))
        add2menu(help_menu,
                 text=_('Report a bug...'),
                 conector_event='activate',
                 conector_action=lambda x: webbrowser.open(
                     'https://bugs.launchpad.net/backlight-indicator'))
        add2menu(help_menu)
        web = add2menu(help_menu,
                       text=_('Homepage'),
                       conector_event='activate',
                       conector_action=lambda x: webbrowser.open(
                           'http://www.atareao.es/tag/backlight-indicator'))
        twitter = add2menu(help_menu,
                           text=_('Follow us in Twitter'),
                           conector_event='activate',
                           conector_action=lambda x: webbrowser.open(
                               'https://twitter.com/atareao'))
        googleplus = add2menu(help_menu,
                              text=_('Follow us in Google+'),
                              conector_event='activate',
                              conector_action=lambda x: webbrowser.open(
                                'https://plus.google.com/\
                                118214486317320563625/posts'))
        facebook = add2menu(help_menu,
                            text=_('Follow us in Facebook'),
                            conector_event='activate',
                            conector_action=lambda x: webbrowser.open(
                                'http://www.facebook.com/elatareao'))
        add2menu(help_menu)
        web.set_image(Gtk.Image.new_from_file(WEBICON))
        web.set_always_show_image(True)
        twitter.set_image(Gtk.Image.new_from_file(TWITTERICON))
        twitter.set_always_show_image(True)
        googleplus.set_image(Gtk.Image.new_from_file(GOOGLEPLUSICON))
        googleplus.set_always_show_image(True)
        facebook.set_image(Gtk.Image.new_from_file(FACEBOOKICON))
        facebook.set_always_show_image(True)
        add2menu(help_menu)
        add2menu(help_menu,
                 text=_('About'),
                 conector_event='activate',
                 conector_action=self.on_about_item)
        help_menu.show()
        return(help_menu)

    def get_menu(self):
        """Create and populate the menu."""
        menu = Gtk.Menu()

        self.working_menu_item = Gtk.MenuItem().new_with_label(_('Start'))
        self.working_menu_item.connect('activate', self.on_working_menu_item)
        self.working_menu_item.show()
        menu.append(self.working_menu_item)
        if self.wid > 0:
            self.working_menu_item.set_label(_('Stop'))
        else:
            self.working_menu_item.set_label(_('Start'))
        menu.append(self.working_menu_item)
        #
        capture_backlight_menu = Gtk.MenuItem().new_with_label(_('Capture \
backlight'))
        capture_backlight_menu.connect('activate',
                                       self.on_capture_backlight_menu)
        capture_backlight_menu.show()
        menu.append(capture_backlight_menu)
        #
        set_backlight_menu = Gtk.MenuItem().new_with_label(_('Set \
backlight manually'))
        set_backlight_menu.connect('activate', self.on_set_backlight_menu)
        set_backlight_menu.show()
        menu.append(set_backlight_menu)
        #
        separator1 = Gtk.SeparatorMenuItem()
        separator1.show()
        menu.append(separator1)
        #
        menu_preferences = Gtk.MenuItem.new_with_label(_('Preferences'))
        menu_preferences.connect('activate', self.on_preferences_item)
        menu_preferences.show()
        menu.append(menu_preferences)

        menu_help = Gtk.MenuItem.new_with_label(_('Help'))
        menu_help.set_submenu(self.get_help_menu())
        menu_help.show()
        menu.append(menu_help)
        #
        separator2 = Gtk.SeparatorMenuItem()
        separator2.show()
        menu.append(separator2)
        #
        menu_exit = Gtk.MenuItem.new_with_label(_('Exit'))
        menu_exit.connect('activate', self.on_quit_item)
        menu_exit.show()
        menu.append(menu_exit)
        #
        menu.show()
        return(menu)

    def set_backlight(self, value, force=False):
        if value == self.backlight:
            return
        if not force:
            if self.change_on_ac and Battery.is_ac():
                if value < self.value_on_ac:
                    value = self.value_on_ac
                else:
                    if value > self.maximum_backlight or value > 100:
                        value = self.maximum_backlight
                    elif value < self.minimum_backlight or value < 0:
                        value = self.minimum_backlight
            elif self.change_on_low_power and\
                    Battery.get_percentage() < self.low_battery_value:
                if value > self.value_on_low_power:
                    value = self.value_on_low_power
                else:
                    if value > self.maximum_backlight or value > 100:
                        value = self.maximum_backlight
                    elif value < self.minimum_backlight or value < 0:
                        value = self.minimum_backlight
            else:
                if value > self.maximum_backlight or value > 100:
                    value = self.maximum_backlight
                elif value < self.minimum_backlight or value < 0:
                    value = self.minimum_backlight
        old_value = self.backlight
        self.backlight = int(value)
        self.backlightManager.set_backlight(self.backlight)
        if self.show_value:
            self.indicator.set_label(str(int(self.backlight)), '')
        else:
            self.indicator.set_label('', '')
        self.indicator.set_icon(comun.STATUS_ICON[self.theme][0])
        if self.show_notifications and\
                int(abs(float(old_value)-float(self.backlight)) /
                    float(self.backlight)) > 5:
            self.notification.update(
                'Backlight-Indicator',
                _('Backlight')+': %s' % self.backlight,
                comun.STATUS_ICON[self.theme][0])
            self.notification.show()

    def on_set_backlight_menu(self, widget):
        sbd = SetBacklightDialog(self.backlight)
        if sbd.run() == Gtk.ResponseType.ACCEPT:
            backlight = sbd.get_selected_backlight()
            sbd.hide()
            self.set_backlight(backlight)
        sbd.destroy()

    def get_backlight_from_webcam(self):
        backlight = self.webcam.get_backlight()
        print('=== captured backlight: %s ===' % (backlight))
        self.set_backlight(backlight)
        return backlight

    def on_capture_backlight_menu(self, widget):
        t = threading.Thread(target=self.get_backlight_from_webcam)
        t.setDaemon(True)
        t.start()

    def start_automatically(self):
        if self.wid != 0:
            GLib.source_remove(self.wid)
            self.wid = 0
        self.working_menu_item.set_label(_('Stop'))
        self.indicator.set_icon(comun.STATUS_ICON[self.theme][0])
        if self.show_notifications:
            self.notification.update('Backlight-Indicator',
                                     _('Session starts'),
                                     comun.STATUS_ICON[self.theme][0])
            self.notification.show()
        self.do_the_work()
        self.wid = GLib.timeout_add_seconds(self.sample_time * 60,
                                            self.do_the_work)

    def on_working_menu_item(self, widget):
        if self.wid == 0:
            self.working_menu_item.set_label(_('Stop'))
            self.indicator.set_icon(comun.STATUS_ICON[self.theme][0])
            if self.show_notifications:
                self.notification.update('Backlight-Indicator',
                                         _('Session starts'),
                                         comun.STATUS_ICON[self.theme][0])
            self.do_the_work()
            self.wid = GLib.timeout_add_seconds(self.sample_time * 60,
                                                self.do_the_work)
        else:
            self.working_menu_item.set_label(_('Start'))
            self.indicator.set_icon(comun.STATUS_ICON[self.theme][1])
            if self.show_notifications:
                self.notification.update('Backlight-Indicator',
                                         _('Session stops'),
                                         comun.STATUS_ICON[self.theme][1])
            GLib.source_remove(self.wid)
            self.wid = 0
        if self.show_notifications:
            self.notification.show()

    def do_the_work(self):
        print(1)
        if self.is_lid_open():   #only update the brigtness-setting if lid is open (no nothing if lid is closed)
            t = threading.Thread(target=self.get_backlight_from_webcam)
            t.setDaemon(True)
            t.start()

        return True

    def is_lid_open(self):
        if os.path.isfile("/proc/acpi/button/lid/LID0/state"):
            #check LID0 for status
            lid_state = subprocess.getoutput(" grep -Po '(?<=^state:).*\w*$' /proc/acpi/button/lid/LID0/state | tr -d '[:space:]'")
            if lid_state == "closed":
                return False
            else:
                return True
        else:
            return True  #ignore check if file does not exist

    def get_about_dialog(self):
        """Create and populate the about dialog."""
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_name(comun.APPNAME)
        about_dialog.set_version(comun.VERSION)
        about_dialog.set_copyright(
            'Copyrignt (c) 2016\nLorenzo Carbonell Cerezo')
        about_dialog.set_comments(_('An indicator to set backlight'))
        about_dialog.set_license('''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
''')
        about_dialog.set_website('http://www.atareao.es')
        about_dialog.set_website_label('http://www.atareao.es')
        about_dialog.set_authors([
            'Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>'])
        about_dialog.set_documenters([
            'Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>'])
        about_dialog.set_translator_credits('''
Lorenzo Carbonell <https://launchpad.net/~lorenzo-carbonell>\n
''')
        about_dialog.set_icon(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
        about_dialog.set_logo(GdkPixbuf.Pixbuf.new_from_file(comun.ICON))
        about_dialog.set_program_name(comun.APPNAME)
        return about_dialog

    # ##################### callbacks for the menu #######################
    def on_preferences_item(self, widget, data=None):
        widget.set_sensitive(False)
        preferences_dialog = PreferencesDialog()
        if preferences_dialog.run() == Gtk.ResponseType.ACCEPT:
            preferences_dialog.hide()
            preferences_dialog.save_preferences()
            self.read_preferences()
            self.indicator.set_icon(self.active_icon)
        preferences_dialog.destroy()
        widget.set_sensitive(True)

    def on_quit_item(self, widget, data=None):
        # self.stop_the_work()
        self.save_preferences()
        exit(0)

    def on_about_item(self, widget, data=None):
        if self.about_dialog:
            self.about_dialog.present()
        else:
            self.about_dialog = self.get_about_dialog()
            self.about_dialog.run()
            self.about_dialog.destroy()
            self.about_dialog = None

#################################################################


def main():
    if dbus.SessionBus().\
                          request_name('es.atareao.BacklightIndicator') != \
                          dbus.bus.REQUEST_NAME_REPLY_PRIMARY_OWNER:
        print("application already running")
        exit(0)
    Notify.init('BacklightIndicator')
    bi = BacklightIndicator()
    print(1)
    loop = GLib.MainLoop()
    print(2)
    loop.run()
    print(3)
    Gtk.main()
    print(4)

if __name__ == "__main__":
    main()
