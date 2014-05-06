import sublime_plugin
from ..utils import *

# Commmand to insert namespace into the active file
class PhexInsertNamespaceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        projectRoot = getProjectRoot()
        sourceRoot = getSourceRoot(projectRoot)
        sourceDir = sourceRoot.replace(projectRoot+os.sep, "")
        namespace = self.view.file_name()
        # Remove path to source directory
        namespace = namespace.replace(sourceRoot+os.sep, '')
        # Remove file extension
        namespace = namespace.replace('.php', '')
        # Replace / with \
        namespace = namespace.replace(os.sep, '\\')
        # Remove class name
        namespace = namespace[0:namespace.rfind('\\')]

        for (ns, dirName) in getComposerData().getPsr4Namespaces().items():
            if dirName == sourceDir:
                namespace = ns+namespace
                break

        loc = self.view.sel()[-1].end()
        self.view.insert(edit, loc, "namespace "+namespace+";")
