import ast
from .extractors import add_missing_attribute
from cloudhive.utils import basename


class TargetNodeVisitor(ast.NodeVisitor):
    def __init__(self, outer):
        self.outer = outer
        self.target_node = None

    def visit_Call(self, node):
        """Search the class in the file"""

        if isinstance(node.func, ast.Name) and node.func.id == self.outer.search_class:
            self.target_node = node
        self.generic_visit(node)


class CraftModifier(ast.NodeTransformer):
    def __init__(self, upper, modify_data):
        self.upper = upper
        self.modify_args = modify_data

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.upper.search_class:
            for keyword in node.keywords:
                if keyword.arg == list(self.modify_args.keys())[0]:
                    keyword.value = dict_to_ast_node(list(self.modify_args.values())[0])

        return self.generic_visit(node)


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


class Transformer:
    def __init__(self, file_path, search_class):
        self.file_path = file_path
        self.search_class = search_class
        self.tree = self._parse_file()

    def _parse_file(self):
        with open(self.file_path, 'r') as f:
            return ast.parse(f.read())

    def find_target_node(self):
        visitor = TargetNodeVisitor(self)
        visitor.visit(self.tree)
        return visitor.target_node

    @add_missing_attribute
    def modify_args(self, **kwargs):
        """Moodify the node attributes"""

        modify = CraftModifier(self, kwargs)
        return modify.visit(self.tree)

    def run_module(self, module):
        exec_globals = {"__name__": "__main__", "__builtins__": __builtins__, "__file__": basename(self.file_path)}

        for node in ast.iter_child_nodes(module):
            if isinstance(node, ast.ImportFrom):
                print(node.module)
                if node.names[0].name == "Crafter":
                    print("Crafter imported")
                    from portcraft.module_utils.basic import Crafter
                    exec_globals['Crafter'] = Crafter

        return exec(compile(module, self.file_path, mode="exec"), exec_globals)
