import ast
import sys
from .converters import add_missing_attribute, dict_to_ast_node
from cloudhive.utils import basename



class CraftModifier(ast.NodeTransformer):
    def __init__(self, upper, modify_data):
        self.upper = upper
        self.modify_args = modify_data

    def visit_Module(self, node):
        init_dict = self._create_dict_initialization("RESULT")
        node.body.insert(0, init_dict)
        return self.generic_visit(node)


    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "exit":
            pass
        return self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id == self.upper.search_class:
                instance_name = node.targets[0].id
                validation_node = self._create_method_call(instance_name, "validate", self.modify_args)
                return [node, validation_node]
        return self.generic_visit(node)

    @staticmethod
    def _create_dict_initialization(name):
        return ast.Assign(
            targets=[ast.Name(id=name,ctx=ast.Store())],
            value=ast.Dict()
        )

    @staticmethod
    def _store_global_variable(name, ref_node):
        return ast.Assign(
            targets=[ast.Name(id=name, ctx=ast.Store())],
            value=ast.Name(id=name, ctx=ast.Load()),
            lineno=ref_node.lineno,
            col_offset=ref_node.col_offset
        )

    @staticmethod
    def _create_method_call(instance_name, method, data):
        return ast.Expr(
            value=ast.Call(
                func=ast.Attribute(
                    value=ast.Name(
                        id=instance_name, ctx=ast.Load()
                    ),
                    attr=method,
                    ctx=ast.Load()
                ),
                args=[dict_to_ast_node(data)]
            )
        )

class Transformer:
    """
    A class to parse and transform an AST from a Python file,
    modify specific class attributes, and execute the modified module.
    """

    def __init__(self, file_path, search_class="Crafter"):
        """
        Initialize the Transformer instance.

        Args:
            file_path (str): Path to the Python file to be parsed.
            search_class (str): The class to search and modify in the AST.
        """

        self.file_path = file_path
        self.search_class = search_class
        self.tree = self._parse_file()

    def _parse_file(self):
        try:
            with open(self.file_path, 'r') as f:
                return ast.parse(f.read())
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{self.file_path}' not found")
        except SyntaxError as e:
            raise SyntaxError(f"Syntax error in file '{self.file_path}': {e}")


    @add_missing_attribute
    def modify_args(self, kwargs):
        """
        Modify the AST nodes for the specified class.

        Args:
            kwargs (dict): Key-value pairs to modify in the target class attributes.

        Returns:
            ast.Module: The modified AST.
        """

        modify = CraftModifier(self, kwargs)
        return modify.visit(self.tree)

    def run_module(self, module):
        """
        Execute the modified module within a controlled namespace.

        Args:
            module (ast.Module): The modified AST to execute.

        Returns:
            None
        """

        exec_globals = {"__name__": "__main__", "__builtins__": __builtins__, "__file__": basename(self.file_path)}
        from portcraft.module_utils.basic import Crafter
        exec_globals['Crafter'] = Crafter
        exec_globals['module_result'] = None

        try:
            compiled_module = compile(module, self.file_path, mode="exec")
            exec(compiled_module, exec_globals)
        except Exception as e:
            print(f"Failed to execute the module {e}")
            sys.exit(0)
            # raise RuntimeError(f"Failed to execute the module {e}")
