import os

TEMPLATES = dict()

def loadTemplate(name, variables = {}):
    content = TEMPLATES.get(name, None)
    if content != None:
        return content

    filename = os.path.dirname(__file__)+os.sep+".."+os.sep+"templates"+os.sep+name+".phex-template"
    content = open(filename).read()

    for (varname, varvalue) in variables.items():
        content = content.replace("%"+varname+"%", varvalue)

    TEMPLATES[name] = content

    return content

def clearTemplateCache():
    TEMPLATES = dict()
