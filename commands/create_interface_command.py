class PhexCreateInterfaceCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Interface name:'

    def on_done(self, input):
        if re.search("^~", input):
            relative = True
            input = re.sub("^~", "", input)
        else:
            relative = False

        namespace_name = getNamespaceName(input, relative)
        filename = getFilenameFromInput(input, namespace_name, relative, True)

        content = loadTemplate("interface", {
            "interface_name":      getInterfaceName(input),
            "namespace_statement": getNamespace(namespace_name),
            "author_phpdoc":       getAuthorPhpDoc(input),
            "copyright_phpdoc":    getCopyrightPhpDoc(input),
            "license_phpdoc":      getLicensePhpDoc(input)
        })

        createPhpFile(filename, content)
