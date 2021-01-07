from .keyboard_layout_provider import KeyboardLayoutProvider
from .language_provider import LanguageProvider
from .widgets import ProgressRow

from gi.repository import Gtk


@Gtk.Template(resource_path='/com/github/p3732/os-installer/ui/pages/keyboard_layout.ui')
class KeyboardLayoutPage(Gtk.Box):
    __gtype_name__ = 'KeyboardLayoutPage'

    stack = Gtk.Template.Child()

    language_list = Gtk.Template.Child()
    layout_list = Gtk.Template.Child()
    language_label = Gtk.Template.Child()

    def __init__(self, global_state, **kwargs):
        super().__init__(**kwargs)

        self.global_state = global_state
        self.loaded_language = ''
        self.language_list_setup = False

        # providers
        self.language_provider = LanguageProvider(global_state)
        self.keyboard_layout_provider = KeyboardLayoutProvider(global_state)

        # signals
        self.language_list.connect('row-activated', self._on_language_row_activated)
        self.layout_list.connect('row-activated', self._on_layout_row_activated)

    def _setup_languages_list(self):
        all_languages = self.language_provider.get_all_languages()

        for language, name in all_languages:
            row = ProgressRow(name, language)
            self.language_list.add(row)

    def _setup_layout_list(self, language, short_hand):
        self._cleanup_layout_list()

        # fill list with all keyboard layouts for given language
        layouts = self.keyboard_layout_provider.get_layouts_for(short_hand)
        assert len(layouts) > 0, 'Language {} has no keyboard layouts! Please report this.'.format(language)
        for keyboard_layout, name in layouts:
            row = ProgressRow(name, keyboard_layout)
            self.layout_list.add(row)

        # set label
        self.language_label.set_label(language)

        self.loaded_language = short_hand

    def _cleanup_layout_list(self):
        # remove all but show all row
        for row in self.layout_list:
            if not row.get_name() == 'show_all_row':
                row.destroy()

    def _select_layout_row(self, list_box, row):
        keyboard_layout = row.get_label()
        short_hand = row.get_info()
        self.global_state.set_keyboard_layout(keyboard_layout, short_hand)
        list_box.select_row(row)

    ### callbacks ###

    def _on_language_row_activated(self, list_box, row):
        # show layouts for language
        language = row.get_label()
        short_hand = row.get_info()
        self._setup_layout_list(language, short_hand)
        self.stack.set_visible_child_name('layouts')

    def _on_layout_row_activated(self, list_box, row):
        if row.get_name() == 'show_all_row':
            # show language selection
            if not self.language_list_setup:
                self._setup_languages_list()
            self.stack.set_visible_child_name('languages')
        else:
            # layout selected
            self._select_layout_row(list_box, row)

    ### public methods ###

    def load(self):
        # load suggested list
        language, short_hand = self.global_state.get_language()
        if not self.loaded_language == short_hand:
            # fill layout list if different language
            self._setup_layout_list(language, short_hand)

            # set current layout to first in list
            row = self.layout_list.get_row_at_index(1)
            self._select_layout_row(self.layout_list, row)

        self.stack.set_visible_child_name('layouts')
        return 'ok_to_proceed'
