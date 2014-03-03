def loadTemplate(name, variables = {}):
    filename = "templates"+os.sep+name+"phex-template"
    content = open(filename)

    for (name, value) in variables.items():
        content.replace("%"+name+"%", value)

    return content
