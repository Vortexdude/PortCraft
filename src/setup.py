import ast
from portcraft.lib.abstract_tree.converters import ast_set_attribute, is_callable_name


def generate_class_structure(class_name, fields):
    class_body = []
    init_args = [ast.arg(arg="self")] + [ast.arg(arg=field) for field in fields]

    init_body = [
        ast.Assign(
            targets=[ast.Attribute(value=ast.Name(id='self', ctx=ast.Load()), attr=field, ctx=ast.Store())],
            value=ast.Name(id=field, ctx=ast.Load())
        )

        for field in fields
    ]

    init_method = ast.FunctionDef(
        name="__init__",
        args=ast.arguments(args=init_args, posonlyargs=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
        body=init_body,
        decorator_list=[]
    )

    class_body.append(init_method)
    class_def = ast.ClassDef(
        name=class_name,
        body=class_body,
        keywords=[],
        bases=[],
        decorator_list=[]
    )

    module = ast.Module(body=[class_def], type_ignores=[])
    ast.fix_missing_locations(module)
    return ast.unparse(module)


# schema = {"Student": ["_id", "name", "email"], "Employee": ["emp_id", "role", "salary"]}

# for _class_name, _fields in schema.items():
#     orm_class = generate_class_structure(_class_name, _fields)
#     print(orm_class)

########################################################################################################
##################################### Skip for now #####################################################
########################################################################################################

code = """

args = {"data": "value"}

class Extractor:
    def __init__(self, argument):
        self.argument = argument
        self.module = None

def run_module():
    xcd = Extractor(args)
    print(f"{xcd.module=}")

run_module()
"""
ext_code = ast.parse(code)
print(ast.dump(ext_code, indent=2))

