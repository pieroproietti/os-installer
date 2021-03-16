# SPDX-License-Identifier: GPL-3.0-or-later

from threading import Lock

from gi.repository import Gtk

from .global_state import global_state
from .installation_scripting import installation_scripting
from .internet_provider import internet_provider
from .page import Page
from .system_calls import open_wifi_settings, start_system_timesync


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/internet.ui')
class InternetPage(Gtk.Box, Page):
    __gtype_name__ = __qualname__
    image_name = 'network-wireless-disabled-symbolic'

    settings_button = Gtk.Template.Child()

    can_proceed_automatically = False
    connected = False
    connected_lock = Lock()

    def __init__(self, **kwargs):
        Gtk.Box.__init__(self, **kwargs)

        # signals
        self.settings_button.connect('clicked', self._on_clicked_settings_button)

    def _set_connected(self):
        self.image_name = 'network-wireless-symbolic'
        start_system_timesync()
        installation_scripting.start_preparation()

    ### callbacks ###

    def _on_clicked_settings_button(self, button):
        open_wifi_settings()

    def _on_connected(self):
        with self.connected_lock:
            self._set_connected()

        # do not hold lock, could cause deadlock with simultaneous load()
        global_state.advance(self.__gtype_name__)

    ### public methods ###

    def load_once(self):
        with self.connected_lock:
            # setup callback on connected
            if internet_provider.is_connected_now_or_later(self._on_connected):
                # already connected
                self._set_connected()
                return True
            if global_state.demo_mode:
                return True
