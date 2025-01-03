import ast
from portcraft.lib.abstract_tree.converters import ast_set_attribute, is_callable_name


class Ext(ast.NodeTransformer):
    def __init__(self):
        self.right_after = 0
        self.search_class = None
        self.class_attribute = None

    def class_setter(self, class_name, value):
        self.search_class = class_name
        self.class_attribute = value

    def _modify_data(self, node):
        attr_key, attr_value = next(iter(self.class_attribute.items()))
        _instance_name = node.targets[0].id  # instance.attribute_key = attribute_value
        return ast_set_attribute(_instance_name, attr_key, attr_value)

    def visit_Assign(self, node):
        if is_callable_name(node) and node.value.func.id == self.search_class:
            new_assignment = self._modify_data(node)
            return [node, new_assignment]
        return node


def modify(pycode: str, search_class, assign_data):
    _data = ast.parse(pycode)
    obj = Ext()
    obj.class_setter(search_class, assign_data)
    modified_ast = obj.visit(_data)
    ast.fix_missing_locations(modified_ast)

    return modified_ast


def run_module(code: str):
    LIB_CLASS = "Extractor"
    INJECTED_DATA = {"module": {"key1": "value1"}}
    exec_globals = {"__name__": "__main__", "__builtins__": __builtins__}
    ast_data = modify(code, LIB_CLASS, INJECTED_DATA)
    exec(compile(ast_data, filename="<nothing>", mode="exec"), exec_globals)


run_module(code)