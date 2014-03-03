import sublime
import sublime_plugin
import os
import re
import json

VIEW_NAME = "Phex"

class Pref:
    @staticmethod
    def load():
        settings = sublime.load_settings('phex.sublime-settings')

        Pref.default_author    = settings.get('phex_default_author')
        Pref.default_copyright = settings.get('phex_default_copyright')
        Pref.default_license   = settings.get('phex_default_license')
        Pref.default_source_dir = settings.get('phex_default_source_dir')

def plugin_loaded():
    Pref.load()

class PhexBase(sublime_plugin.WindowCommand):
    def display_results(self):
        display = ShowInPanel(self.window)
        display.display_results()

    def window(self):
        return self.view.window()

class PhexInputBase(PhexBase):
    def run(self):
        self.input_panel_view = self.window.show_input_panel(
            self.INPUT_PANEL_CAPTION,
            "",
            self.on_done,
            self.on_update,
            self.on_cancel
        )

        self.input_panel_view.set_name(VIEW_NAME)
        self.input_panel_view.settings().set("auto_complete_commit_on_tab", False)
        self.input_panel_view.settings().set("tab_completion", False)
        self.input_panel_view.settings().set("translate_tabs_to_spaces", False)
        self.input_panel_view.settings().set("anf_panel", True)
        self.view = self.window.active_view()

    def on_update(self, input):
        match = getNamespaceAutocompletion(input)

        if not match == None:
            self.input_panel_view.run_command("anf_replace", {"content": match})
        else:
            pass

    def on_cancel(self):
        pass
