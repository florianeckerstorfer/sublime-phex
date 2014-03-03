class PhexCreateClassCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Class name:'

    def on_done(self, input):
        content = "<?php\n\n%namespace%/**\n * %class_name%\n *\n%author%%copyright%%license% */\nclass %class_name%\n{\n}\n"
        if re.search("^~", input):
            relative = True
            input = re.sub("^~", "", input)
        else:
            relative = False

        namespace_name = getNamespaceName(input, relative)
        filename = getFilenameFromInput(input, namespace_name, relative, False)

        content = content.replace("%class_name%", getClassName(input))
        content = content.replace("%namespace%", getNamespace(namespace_name))
        content = content.replace("%author%", getAuthorPhpDoc(input))
        content = content.replace("%copyright%", getCopyrightPhpDoc(input))
        content = content.replace("%license%", getLicensePhpDoc(input))

        createPhpFile(filename, content)

    def on_update(self, input):
        match = getNamespaceAutocompletion(input)

        if not match == None:
            self.input_panel_view.run_command("anf_replace", {"content": match})
        else:
            pass

    def on_cancel(self):
        pass
