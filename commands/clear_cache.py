import sublime_plugin
from ..utils import *

class PhexClearCacheCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        clearTemplateCache()
        clearComposerCache()
