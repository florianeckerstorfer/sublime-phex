import sublime_plugin
import re
import os
from ..utils import *

class PhexInsertClassNameCommand(sublime_plugin.TextCommand):
    php_files = []
    class_names = []
    def run(self, edit):
        self.php_files = []
        self.class_names = []

        pattern = re.compile("^(app|src|lib|libs|vendor).*\.php$")
        root_dir = self.view.window().folders()[0] + os.sep
        for dirpath, sub_folders, files in os.walk(root_dir):
            for file in files:
                filename = os.path.join(dirpath, file).replace(root_dir, "")
                if pattern.search(filename):
                    self.php_files.append(filename)
                    self.class_names.append(filenameToClassName(filename))
        self.view.window().show_quick_panel(self.class_names, self.on_select)

    def on_select(self, input):
        root_dir = self.view.window().folders()[0] + os.sep
        content = open(root_dir + self.php_files[input]).read()
        namespaces = re.compile("namespace (.*?);").findall(content)
        names = re.compile("(class|interface) ([a-zA-Z0-9_]*)").findall(content)

        class_name = ""
        try:
            class_name += namespaces[0]+"\\"
        except IndexError:
            pass
        try:
            class_name += names[0][1]
        except IndexError:
            pass

        self.view.run_command("phex_insert_class_name_execute", {"class_name": class_name})

class PhexInsertClassNameExecuteCommand(sublime_plugin.TextCommand):
    def run(self, edit, class_name):
        # Replace each selection with the class name
        for region in self.view.sel():
            self.view.replace(edit, region, class_name)
