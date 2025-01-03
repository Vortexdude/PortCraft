import ast


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
