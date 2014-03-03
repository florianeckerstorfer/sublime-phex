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
