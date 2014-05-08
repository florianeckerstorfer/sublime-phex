import sublime_plugin
import re
from .base import *
from ..utils import *

class PhexCreatePropertyCommand(PhexInputBase):
    INPUT_PANEL_CAPTION = 'Property name:'

    def on_done(self, property_name):
        # Check if the user provided a type. Type must be of the form "TYPE PROPERTY_NAME"
        # The type defaults to "string"
        if property_name.find(" ") == -1:
            type = "string"
        else:
            (type, property_name) = property_name.split(" ")

        # Get the content of the view
        content = self.view.substr(sublime.Region(0, self.view.size()))

        # Find the class name (used for the @return of setter)
        m = re.search(r"class\s+([a-zA-Z0-9_]+)", content)
        class_name = m.group(1)

        # Find the position where to insert the property code
        position = None
        first = False
        for m in re.finditer(r"(public|protected|private) \$[a-zA-Z0-9_]+;", content):
            position = m.end()

        if position == None:
            for m in re.finditer(r"class[a-zA-Z0-9_ ]+\s*\n?{", content):
                position = m.end()
                first = True

        # If there exist properties in the code, we prepend an additional line break
        property_code = self.get_property_code(type, property_name)
        if not first:
            property_code = "\n"+property_code

        # Insert property definition
        self.view.run_command("phex_insert_text_in_view", {
            "position": position,
            "buffer": property_code
        })

        # Get the updated version of the code
        content = self.view.substr(sublime.Region(0, self.view.size()))

        position = content.rfind("}")

        self.view.run_command("phex_insert_text_in_view", {
            "position": position,
            "buffer": self.get_setter_getter_code(type, property_name, class_name)
        })

    def get_property_code(self, type, property_name):
        code = "\n"
        code += "    /** @var "+type+" **/\n"
        code += "    private $"+property_name
        if type == "array" or type[-2:] == "[]":
            code += " = []"
        code += ";"

        return code

    def get_setter_getter_code(self, type, property_name, class_name):
        typehint = ""
        if type[-2:] == "[]":
            typehint = "array "
        elif type not in ['int', 'integer', 'string', 'bool', 'boolean', 'mixed']:
            typehint = type+" "

        code = "\n"
        code += "    /**\n"
        code += "     * @param "+type+" $"+property_name+"\n"
        code += "     *\n"
        code += "     * @return "+class_name+"\n"
        code += "     */\n"
        code += "    public function set"+property_name.capitalize()+"("+typehint+"$"+property_name+")\n"
        code += "    {\n"
        code += "        $this->"+property_name+" = $"+property_name+";\n\n"
        code += "        return $this;\n"
        code += "    }\n\n"
        code += "    /**\n"
        code += "     * @return "+type+"\n"
        code += "     */\n"
        code += "    public function get"+property_name.capitalize()+"()\n"
        code += "    {\n"
        code += "        return $this->"+property_name+";\n"
        code += "    }\n"
        return code

class PhexInsertTextInViewCommand(sublime_plugin.TextCommand):
    def run(self, edit, position, buffer):
        self.view.insert(edit, position, buffer)
