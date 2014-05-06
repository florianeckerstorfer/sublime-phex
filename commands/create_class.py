import re
from .base import *
from ..utils import *

class PhexCreateClassCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Class name:'

    def on_done(self, input):
        if re.search("^~", input):
            relative = True
            input = re.sub("^~", "", input)
        else:
            relative = False

        namespace_name = getNamespaceName(input, relative)
        filename = getFilenameFromInput(input, namespace_name, relative, False)

        content = loadTemplate("class", {
            "class_name":          getClassName(input),
            "namespace_statement": getNamespace(namespace_name),
            "package_phpdoc":      getPackagePhpDoc(input),
            "author_phpdoc":       getAuthorPhpDoc(input),
            "copyright_phpdoc":    getCopyrightPhpDoc(input),
            "license_phpdoc":      getLicensePhpDoc(input)
        })

        createPhpFile(filename, content)
