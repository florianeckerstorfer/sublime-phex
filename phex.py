import sublime
import sublime_plugin
import os
import re

class Pref:
    @staticmethod
    def load():
        settings = sublime.load_settings('phex.sublime-settings')

        Pref.default_author    = settings.get('phex_default_author')
        Pref.default_copyright = settings.get('phex_default_copyright')
        Pref.default_license   = settings.get('phex_default_license')

def plugin_loaded():
    Pref.load()

class PhexBase(sublime_plugin.WindowCommand):
    def display_results(self):
        display = ShowInPanel(self.window)
        display.display_results()

    def window(self):
        return self.view.window()

    def run_shell_command(self, command, working_dir):
        if not command:
            return False

        if working_dir == '/' or working_dir == '':
            sublime.status_message('You\'re not in a Symfony2 application.')
            return

        self.view.window().run_command("exec", {
            "cmd": command,
            "shell": False,
            "working_dir": working_dir,
            "file_regex": ""
        })
        self.display_results()
        return True

    def build_cmd(self, cmd):
        cmd.insert(0, Pref.php_bin)
        cmd.insert(1, Pref.console_bin)
        cmd.append('--no-interaction')

        return cmd


class PhexInputBase(PhexBase):
    def run(self):
        self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.on_done, None, None)
        self.view = self.window.active_view()

class PhexCreateClassCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Class name:'

    def on_done(self, text):
        content = "<?php\n\n%namespace%/**\n * %class_name%\n *\n%author%%copyright%%license% */\nclass %class_name%\n{\n}\n"
        filename = text.replace("\\", "/") + ".php"
        class_name_start = text.rfind("\\")
        if class_name_start == -1:
            class_name_start = 0
        if text[(class_name_start)] == "\\":
            class_name = text[(class_name_start+1):]
        else:
            class_name = text[class_name_start:]
        namespace_name = text[:class_name_start]
        namespace = ""
        if len(namespace_name) > 0:
            namespace = "namespace "+namespace_name+";\n\n"

        author = ""
        if Pref.default_author:
            author = " * @author    "+Pref.default_author+"\n"
        copyright = ""
        if Pref.default_copyright:
            copyright = " * @copyright "+Pref.default_copyright+"\n"
        license = ""
        if Pref.default_license:
            license = " * @license   "+Pref.default_license+"\n"

        content = content.replace("%class_name%", class_name)
        content = content.replace("%namespace%", namespace)
        content = content.replace("%author%", author)
        content = content.replace("%copyright%", copyright)
        content = content.replace("%license%", license)

        createClassFile(filename, content, "Path does not exist.")

def createClassFile(file, contents, msg):
    if contents is None:
        return
    if os.path.exists(file):
        sublime.error_message(msg)
        return
    open(file, "w")
    view = sublime.active_window().open_file(file)
    view.set_syntax_file("Packages/php-extended/PHP.tmLanguage")
    sublime.set_timeout(lambda: insertAndSave(view, contents), 100)

def insertAndSave(view, contents):
    view.run_command("insert_snippet", {"contents": contents})
    view.run_command("save")

