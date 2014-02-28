import sublime
import sublime_plugin
import os
import re
import json

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
        self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.on_done, None, None)
        self.view = self.window.active_view()


class PhexCreateClassCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Class name:'

    def on_done(self, input):
        content = "<?php\n\n%namespace%/**\n * %class_name%\n *\n%author%%copyright%%license% */\nclass %class_name%\n{\n}\n"
        if re.search("^~", input):
            relative = True
            input = re.sub("^~", "", input)
        else:
            relative = False

        namespace_name = getNamespaceName(input, relative)
        filename = getFilenameFromInput(input, namespace_name, relative, False)

        content = content.replace("%class_name%", getClassName(input))
        content = content.replace("%namespace%", getNamespace(namespace_name))
        content = content.replace("%author%", getAuthorPhpDoc(input))
        content = content.replace("%copyright%", getCopyrightPhpDoc(input))
        content = content.replace("%license%", getLicensePhpDoc(input))

        createPhpFile(filename, content)

class PhexCreateInterfaceCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Interface name:'

    def on_done(self, input):
        content = "<?php\n\n%namespace%/**\n * %interface_name%\n *\n%author%%copyright%%license% */\ninterface %interface_name%\n{\n}\n"

        if re.search("^~", input):
            relative = True
            input = re.sub("^~", "", input)
        else:
            relative = False

        namespace_name = getNamespaceName(input, relative)
        filename = getFilenameFromInput(input, namespace_name, relative, True)

        content = content.replace("%interface_name%", getInterfaceName(input))
        content = content.replace("%namespace%", getNamespace(namespace_name))
        content = content.replace("%author%", getAuthorPhpDoc(input))
        content = content.replace("%copyright%", getCopyrightPhpDoc(input))
        content = content.replace("%license%", getLicensePhpDoc(input))

        createPhpFile(filename, content)


def getProjectSetting(setting_name):
    data = getProjectData()
    try:
        return data["settings"][setting_name]
    except KeyError:
        return None

def getProjectRoot():
    if sublime.active_window().project_file_name() is not None:
        data = sublime.active_window().project_data()
        current_dir = os.path.realpath(
            os.path.dirname(sublime.active_window().project_file_name())+"/"+data["folders"][0]["path"]
        )
    else:
        current_dir = getWorkingDirectory()
        if not current_dir:
            sublime.message_dialog("Could not find project root or current working directory.")
            return None

        while current_dir is not "/" and not isRootDir(current_dir):
            current_dir = os.path.dirname(current_dir)

    return current_dir

def isRootDir(root_dir):
    if os.path.exists(root_dir+"/.sublime-project"):
        return True

    if os.path.exists(root_dir+"/.composer.json"):
        return True

    if os.path.exists(root_dir+"/src"):
        return True

    if os.path.exists(root_dir+"/lib"):
        return True

    return False

def getSourceDir(project_root):
    source_dir = getProjectSetting("source_dir")
    if source_dir and os.path.exists(project_root+"/"+source_dir):
        return source_dir

    source_dir = Pref.default_source_dir
    if source_dir and os.path.exists(project_root+"/"+source_dir):
        return source_dir

    source_dir = "src"
    if os.path.exists(project_root+"/"+source_dir):
        return source_dir

    source_dir = "lib"
    if os.path.exists(project_root+"/"+source_dir):
        return source_dir

    return ""

def getSourceRoot(project_root):
    source_dir = getSourceDir(project_root)
    if source_dir:
        source_dir = "/"+source_dir

    return project_root+source_dir

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
def getNamespace(namespace_name):
    namespace = ""
    if len(namespace_name) > 0:
        namespace = "namespace "+namespace_name+";\n\n"

    return namespace

def getNamespaceName(input, relative = False):
    class_name_start = getClassNameStart(input)

    namespace_name = input[:class_name_start]

    if relative:
        prefix = getWorkingDirectory().replace(getSourceRoot(getProjectRoot())+"/", "")
        sublime.message_dialog("prefix: "+prefix)
        if len(prefix) > 0:
            if len(namespace_name) > 0:
                prefix += "\\"
            namespace_name = prefix+namespace_name

    return namespace_name

"""
    Returns the filename for the given input.
    The input is most likely a class name (with our without namespace).
    However, it can also be prefixed with ~

    If the input is prefixed with `~` return the path based on the currently active view, otherwise return the path
    based from the guessted base directory.
"""
def getFilenameFromInput(input, namespace, relative = False, interface = False):
    if relative:
        path = getCurrentDirectory()
    else:
        path = getSourceRoot(getProjectRoot())
        psr4Namespaces = getComposerPsr4Namespaces()
        for (ns, nspath) in psr4Namespaces.items():
            ns = re.sub("\\$", "", ns)
            namespace += "\\"
            if namespace.find(ns) == 0:
                input = input.replace(ns, "")

    interface_part = ""
    if interface:
        interface_part = "Interface"

    return path+"/"+input.replace("\\", "/")+interface_part+".php"

def getProjectData():
    if sublime.active_window().project_file_name() is not None:
        return sublime.active_window().project_data()

    return {}

"""
    Returns the directory of the currently active file.
"""
def getWorkingDirectory():
    if not sublime.active_window():
        return None
    if not sublime.active_window().active_view():
        return None
    if not sublime.active_window().active_view().file_name():
        return None

    return os.path.realpath(os.path.dirname(sublime.active_window().active_view().file_name()))

"""
    Returns the data from Composer file
"""
def getComposerData():
    current_dir = getCurrentDirectory()
    if not current_dir:
        current_dir = getProjectRoot()

    while not current_dir == "/" and not os.path.exists(current_dir+"/composer.json"):
        current_dir = os.path.dirname(current_dir)

    composerFilename = current_dir+"/composer.json"
    if not os.path.exists(composerFilename):
        return null

    json_data=open(composerFilename)
    data = json.load(json_data)
    json_data.close()

    return data

def getComposerPsr4Namespaces():
    data = getComposerData()
    try:
        namespaces = {}
        for (namespace, path) in data["autoload"]["psr-4"].items():
            namespaces[namespace] = path
        return namespaces
    except KeyError:
        return {}

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

# class PhexTestCommand(sublime_plugin.WindowCommand):
#     def run(self):
#         project_root = getProjectRoot()
#         sublime.message_dialog("project_root: "+project_root)
#         sublime.message_dialog("source_dir: "+getSourceDir(project_root))
#         sublime.message_dialog("source_root: "+getSourceRoot(project_root))

