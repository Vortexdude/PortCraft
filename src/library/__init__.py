import ast
from src.lib.transformers import CraftModifier


new_args = {
    "action": "create",
    "repo": "DockCraft",
    "branch": "master",
    "commit": "No",  # Example: adding a new key
}


class Extractor:
    def __init__(self, struc):
        self.tree = struc
        self._functions = []
        self._classes = []
        self.run()

    @property
    def functions(self):
        return self._functions

    @property
    def classes(self):
        return self._classes

    @staticmethod
    def show_info(function_node):
        """Same goes for the class methods as well"""

        print(f"Function Name: {function_node.name}")
        print(f"args: ")
        for arg in function_node.args.args:
            print("\tParameter name:", arg.arg)

    def run(self):
        for n in self.tree.body:
            if isinstance(n, ast.FunctionDef):
                self._functions.append(n)
            elif isinstance(n, ast.ClassDef):
                self._classes.append(n)


with open("GitPy.py", 'r') as f:
    data = f.read()

tree = ast.parse(data)

modifier = CraftModifier()
modifier.new_args = new_args
new_data = modifier.visit(tree)
ast.fix_missing_locations(new_data)

exec(compile(new_data, "<exec 12>", mode="exec"))
