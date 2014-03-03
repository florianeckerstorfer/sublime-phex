"""
    Returns the project setting with the given name.
"""
def getProjectSetting(setting_name):
    data = getProjectData()
    try:
        return data["settings"][setting_name]
    except KeyError:
        return None

"""
    Returns the project data.
"""
def getProjectData():
    if sublime.active_window().project_file_name() is not None:
        return sublime.active_window().project_data()

    return {}

"""
    Returns the project root.
"""
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

"""
    Returns whether the given directory is the project root directory.
"""
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

"""
    Returns the name of the source directory. This is only the directory name, not the full path.
"""
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

"""
    Returns the full path to the source directory.
"""
def getSourceRoot(project_root):
    source_dir = getSourceDir(project_root)
    if source_dir:
        source_dir = "/"+source_dir

    return project_root+source_dir

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
    Returns the data from Composer file.
"""
def getComposerData():
    current_dir = getWorkingDirectory()
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

"""
    Returns the PSR-4 namespaces from the Composer file.
"""
def getComposerPsr4Namespaces():
    data = getComposerData()
    try:
        namespaces = {}
        for (namespace, path) in data["autoload"]["psr-4"].items():
            namespaces[namespace] = path
        return namespaces
    except KeyError:
        return {}
