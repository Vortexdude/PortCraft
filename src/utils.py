import importlib
from .settings import paths
import ast


def import_module(_mod, search_paths:list=None):
    """
    Dynamically imports a module and retrieves a class or attribute.

    Args:
        _mod (str): The name of the class or attribute to import.

        search_paths (list): list of the paths.

    Returns:
        Any: The imported class or attribute, or None if not found.
    """
    if not search_paths:
        search_paths = paths.library_paths

    for library_path in search_paths:
        try:
            module = importlib.import_module(library_path)
            if hasattr(module, _mod):
                return getattr(module, _mod)

        except ImportError:
            print(f"Failed to import module '{library_path}'. Skipping...")

        except AttributeError:
            print(f"'{_mod}' not found in '{library_path}'. Skipping...")

    print(f"'{_mod}' could not be found in any of the provided library paths.")
    return None


class AssignmentCounter(ast.NodeVisitor):
    def __init__(self):
        self.count = 0

    def visit_Assign(self, node):
        super().generic_visit(node)

    def visit_FunctionDef(self, node):
        self.count += 1
        print(f"Found function: {node.name}")
        super().generic_visit(node)

    def visit_Import(self, node):
        print(f"Found import: {node.name}")
        super().generic_visit(node)

    def visit_ImportFrom(self, node):
        for mod in node.names:
            methods = mod.__dict__
            if mod.name == "Crafter":
                print("Module is imported")

        super().generic_visit(node)
