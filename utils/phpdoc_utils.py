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
