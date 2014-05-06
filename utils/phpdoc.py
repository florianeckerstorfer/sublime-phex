from .project import *
from .pref import *

"""
    Returns the @author PHPDoc
"""
def getAuthorPhpDoc(input):
    author = ""
    if getProjectSetting("author"):
        author = getProjectSetting("author")
    elif Pref.default_author:
        author = Pref.default_author

    author_string = ""
    if author:
        author_string = " * @author    "+author+"\n"

    return author_string

"""
    Returns the @copyright PHPDoc
"""
def getCopyrightPhpDoc(input):
    copyright = ""
    if getProjectSetting("copyright"):
        copyright = getProjectSetting("copyright")
    elif Pref.default_copyright:
        copyright = Pref.default_copyright

    copyright_string = ""
    if copyright:
        copyright_string = " * @copyright "+copyright+"\n"

    return copyright_string

"""
    Returns the @license PHPDoc
"""
def getLicensePhpDoc(input):
    license = ""
    if getProjectSetting("license"):
        license = getProjectSetting("license")
    elif Pref.default_license:
        license = Pref.default_license

    license_string = ""
    if license:
        license_string = " * @license   "+license+"\n"

    return license_string

"""
    Returns the @package PHPDoc
"""
def getPackagePhpDoc(input):
    package = ""
    if getProjectSetting("package"):
        package = getProjectSetting("package")

    package_string = ""
    if package:
        package_string = " * @package   "+package+"\n"

    return package_string
