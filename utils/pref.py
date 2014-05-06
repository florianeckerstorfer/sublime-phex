import sublime

class Pref:
    @staticmethod
    def load():
        settings = sublime.load_settings('phex.sublime-settings')

        Pref.default_author     = settings.get('phex_default_author')
        Pref.default_copyright  = settings.get('phex_default_copyright')
        Pref.default_license    = settings.get('phex_default_license')
        Pref.default_source_dir = settings.get('phex_default_source_dir')
