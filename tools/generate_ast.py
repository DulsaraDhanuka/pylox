import os

def generate_ast(output_dir, basename, types) -> None:
    output = ""
    output += "from scanner import Token\n"
    output += "from abc import ABC, abstractmethod\n\n"
    output += define_visitor(basename, types)
    output += f"class {basename}(ABC):\n"
    output += "    @abstractmethod\n"
    output += "    def accept(self, visitor: Visitor) -> object:\n"
    output += "        pass\n"
    for _type in types:
        output += define_type(_type, basename)
    output += ""
    with open(os.path.join(output_dir, f"{basename.lower()}.py"), "w") as f:
        f.write(output)

def define_visitor(basename, types) -> str:
    output = ""
    output += "class Visitor(ABC):\n"
    for _type in types:
        _type = _type.split(":")
        typename, _ = _type[0].strip(), _type[1].split(",")
        output += "    @abstractmethod\n"
        output += f"    def visit_{typename.lower()}_{basename.lower()}(self, expr: {typename}) -> object:\n"
        output += "        pass\n"
    return output

def define_type(_type, basename) -> str:
    _type = _type.split(":")
    classname, fields = _type[0].strip(), _type[1].split(",")
    output = ""
    output += f"class {classname}(object):\n"
    parameters = []
    init = []
    for field in fields:
        field = field.strip().split(" ")
        fieldtype = field[0]
        fieldname = field[1]
        parameters += [f"{fieldname}: {fieldtype}"]
        init += [f"self.{fieldname}: {fieldtype} = {fieldname}"]
    parameters = ", ".join(parameters)
    output += f"    def __init__(self, {parameters}) -> None:\n"
    output += "        " + "\n        ".join(init) + "\n"
    output += "    def accept(self, visitor: Visitor) -> object:\n"
    output += f"        return visitor.visit_{classname.lower()}_{basename.lower()}(self)\n"
    return output


if __name__ == "__main__":
    types = []
    types += ["Binary: Expr left, Token operator, Expr right"]
    types += ["Unary: Token operator, Expr right"]
    types += ["Grouping: Expr expression"]
    types += ["Literal: object value"]
    generate_ast(".", "Expr", types)

