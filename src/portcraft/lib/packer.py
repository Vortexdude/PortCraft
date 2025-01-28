import json
import importlib
from portcraft.settings import pu


def exec_mod(library, method=None, data=None):
    if data:
        import sys
        from io import StringIO

        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)

        sys.stdin = StringIO(data)

    if not method:
        method = "__main__"

    m_spec = importlib.util.spec_from_file_location(method, library)
    module = importlib.util.module_from_spec(m_spec)
    try:

        m_spec.loader.exec_module(module)
        return 0
    except SystemExit as e:
        return e.code


def load_and_run_module(module_name: str, module_path=None, data=None):
    if not module_name:
        raise Exception("'Module_name', shouldn't be empty.")

    if not module_path:
        module_path = pu.library_paths[0]

    if module_name.endswith(".py"):
        library = module_path / module_name
    else:
        library = module_path / f"{module_name}.py"

    return exec_mod(library, data=data)


class TaskPacker:
    def __init__(self, module_name, module_args, module_plugins: dict = None, module_comment=None, e_vars=None, *args, **kwargs):
        self._name = module_name
        self._args = module_args
        self._plugins = module_plugins
        self._vars = e_vars
        self._comment = module_comment
        self.context = kwargs.get('context')

    def run_run(self):
        """Test the module before run load the module and """
        pass

    def run(self):
        for plugin_name, plugin_args in self._plugins.items():
            print(f"Discovering plugin '{plugin_name}' with arg '{plugin_args}'")

        # print(default_console.inject(module_name=self._name, module_comment=self._comment))
        code = load_and_run_module(self._name, data=self._args)
        return code
