import ast

MODULE_CLASS = "Crafter"
MODULE_ARGUMENT_NAME = "module_args"


def dict_to_ast_node(parsed_data: dict):
    if isinstance(parsed_data, dict):
        return ast.Dict(
            keys=[ast.Constant(key) for key in parsed_data.keys()],
            values=[dict_to_ast_node(value) for value in parsed_data.values()]
        )
    elif isinstance(parsed_data, str) or isinstance(parsed_data, bool):
        return ast.Constant(parsed_data)
    else:
        raise ValueError(f"Unsupported Type {type(parsed_data)}")


def _search_class(node, class_name):
    """Search the class in a name and return node"""
    if isinstance(node.func, ast.Name) and node.func.id == class_name:
        print(f"Found the {class_name} Class")
        return True
    return False


def _search_key(node, key):
    for _key in node.keywords:
        if _key.arg == key:
            return True
    return False


def _replace_keyword(node, key, value):
    """Replace the keyword in a node """
    for keyword in node.keywords:  # add condition for change for keyword also
        if keyword.arg == key:
            keyword.value = dict_to_ast_node(value)
    return node


class CraftModifier(ast.NodeTransformer):
    new_args = None

    def visit_Call(self, node):
        if _search_class(node, MODULE_CLASS):
            node = _replace_keyword(node, MODULE_ARGUMENT_NAME, self.new_args)

        return self.generic_visit(node)
