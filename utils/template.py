import os

def loadTemplate(name, variables = {}):
    filename = os.path.dirname(__file__)+os.sep+".."+os.sep+"templates"+os.sep+name+".phex-template"
    content = open(filename).read()

    for (name, value) in variables.items():
        content = content.replace("%"+name+"%", value)

    return content
