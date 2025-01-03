import ast
from .converters import add_missing_attribute, dict_to_ast_node
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


def extract_keywords(node):
    if not isinstance(node, ast.Call):
        raise Exception("Provided node is not Callable")
    keywords = {}
    for keyword in node.keywords:
        if keyword.arg is not None:
            try:
                value = ast.literal_eval(keyword.value)
            except ValueError:
                value = keyword.value
            keywords[keyword] = value

    return keywords


class CraftModifier(ast.NodeTransformer):
    def __init__(self, upper, modify_data):
        self.upper = upper
        self.modify_args = modify_data

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == self.upper.search_class:
            data = extract_keywords(node)
            for keyword in node.keywords:
                if keyword.arg == list(self.modify_args.keys())[0]:
                    keyword.value = dict_to_ast_node(list(self.modify_args.values())[0])

        return self.generic_visit(node)


class Transformer:
    def __init__(self, file_path, search_class):
        self.file_path = file_path
        self.search_class = search_class
        self.tree = self._parse_file()
        self.find_attrs = []

    def find_import_class(self, class_name):
        self.find_attrs.append({class_name: ast.ImportFrom})


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
            for item in self.find_attrs:
                key, value = next(iter(item.items()))
                if isinstance(node, value) and node.names[0].name == key:
                    print("Crafter imported")
                    from portcraft.module_utils.basic import Crafter
                    exec_globals['Crafter'] = Crafter

        return exec(compile(module, self.file_path, mode="exec"), exec_globals)
