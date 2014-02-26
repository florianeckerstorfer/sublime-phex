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

    def on_done(self, input):
        content = "<?php\n\n%namespace%/**\n * %class_name%\n *\n%author%%copyright%%license% */\nclass %class_name%\n{\n}\n"
        filename = getFilenameFromInput(input)

        # Remove the ~ (if it exists) from the beginning of the input
        input = re.sub("^~", "", input)

        content = content.replace("%class_name%", getClassName(input))
        content = content.replace("%namespace%", getNamespace(input))
        content = content.replace("%author%", getAuthorPhpDoc(input))
        content = content.replace("%copyright%", getCopyrightPhpDoc(input))
        content = content.replace("%license%", getLicensePhpDoc(input))

        createPhpFile(filename, content)

class PhexCreateInterfaceCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Interface name:'

    def on_done(self, input):
        content = "<?php\n\n%namespace%/**\n * %interface_name%\n *\n%author%%copyright%%license% */\ninterface %interface_name%\n{\n}\n"
        filename = getFilenameFromInput(input)

        # Remove the ~ (if it exists) from the beginning of the input
        input = re.sub("^~", "", input)

        content = content.replace("%interface_name%", getInterfaceName(input))
        content = content.replace("%namespace%", getNamespace(input))
        content = content.replace("%author%", getAuthorPhpDoc(input))
        content = content.replace("%copyright%", getCopyrightPhpDoc(input))
        content = content.replace("%license%", getLicensePhpDoc(input))

        createPhpFile(filename, content)

"""
    Returns the @author PHPDoc
"""
def getAuthorPhpDoc(input):
    author = ""
    if Pref.default_author:
        author = " * @author    "+Pref.default_author+"\n"

    return author

"""
    Returns the @copyright PHPDoc
"""
def getCopyrightPhpDoc(input):
    copyright = ""
    if Pref.default_copyright:
        copyright = " * @copyright "+Pref.default_copyright+"\n"

    return copyright

"""
    Returns the @license PHPDoc
"""
def getLicensePhpDoc(input):
    license = ""
    if Pref.default_license:
        license = " * @license   "+Pref.default_license+"\n"

    return license

"""
    Returns the index of the character where the class name starts
"""
def getClassNameStart(input):
    class_name_start = input.rfind("\\")
    if class_name_start == -1:
        class_name_start = 0

    return class_name_start

"""
    Returns the class name of the given input.

    Mostly what this method does is removing the namespace.
"""
def getClassName(input):
    class_name_start = getClassNameStart(input)

    if input[(class_name_start)] == "\\":
        return input[(class_name_start+1):]
    else:
        return input[class_name_start:]

"""
    Returns the interface name of the given input.
"""
def getInterfaceName(input):
    return getClassName(input)+"Interface"

"""
    Returns the namespace from the given input.

    The returned string includes the namespace statement.
"""
def getNamespace(input):
    class_name_start = getClassNameStart(input)

    namespace_name = input[:class_name_start]
    namespace = ""
    if len(namespace_name) > 0:
        namespace = "namespace "+namespace_name+";\n\n"

    return namespace

"""
    Returns the filename for the given input.
    The input is most likely a class name (with our without namespace).
    However, it can also be prefixed with ~

    If the input is prefixed with `~` return the path based on the currently active view, otherwise return the path
    based from the guessted base directory.
"""
def getFilenameFromInput(input):
    if re.search("^~", input):
        input = re.sub("^~", "", input)
        path = getCurrentDirectory()
    else:
        path = getBaseDirectory()

    return path+"/"+input.replace("\\", "/") + ".php"

"""
    Returns the base directory.
"""
def getBaseDirectory():
    data = sublime.active_window().project_data()
    path = os.path.realpath(
        os.path.dirname(sublime.active_window().project_file_name())+"/"+data["folders"][0]["path"]
    )

    if os.path.exists(path+"/src"):
        path += "/src"

    return path

"""
    Returns the directory of the currently active file.
"""
def getCurrentDirectory():
    return os.path.realpath(os.path.dirname(sublime.active_window().active_view().file_name()))


# class PhexTestCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         sublime.message_dialog(getCurrentDirectory())

"""
    Creates the given file (and the directory if necessary) and writes the content to it.
    It also sets the syntax highlighting to PHP
"""
def createPhpFile(file, contents):
    if contents is None:
        return
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    open(file, "w")
    view = sublime.active_window().open_file(file)
    view.set_syntax_file("Packages/php-extended/PHP.tmLanguage")
    sublime.set_timeout(lambda: insertAndSave(view, contents), 100)

"""
    Inserts the content in the view and saves the view.
"""
def insertAndSave(view, contents):
    view.run_command("insert_snippet", {"contents": contents})
    view.run_command("save")

