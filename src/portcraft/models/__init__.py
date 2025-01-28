import os.path

from portcraft.lib.common import find_module_file
from portcraft.settings import pu


class Module:
    def __init__(self, attrs):
        self._attrs = attrs
        self._name: str | None = None
        self._comment = None
        self._module_args = {}
        self._plugins = {}
        self.format()
        if not self._name:
            raise ValueError(f"No module defined in the config.")

        self._module_file = find_module_file(self._name, pu.library_paths)
        if not self._module_file:
            raise FileNotFoundError(f"Module not found '{self._name}'")

    @staticmethod
    def checker(key):
        for item in pu.library_paths:
            lib_file_slug = os.path.join(item, key)
            if os.path.exists(lib_file_slug):
                print(f"its {key} a module")
        for item in pu.plugins_path:
            plugin_file_slug = os.path.join(item, key)
            if os.path.exists(plugin_file_slug):
                print(f"its {key} a lib")


    def format(self):
        for key, value in self._attrs.items():
            self.checker(key)
            if key == "name":  # grab the comment if possible
                self._comment = value
            elif isinstance(value, dict):  # check for the args for the module
                self._name = key
                self._module_args = value
            else:
                self._plugins[key] = value

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def name(self) -> str:
        return self._name

    @property
    def args(self):
        return self._module_args

    @property
    def plugins(self) -> dict:
        return self._plugins

    @property
    def file(self) -> str:
        return self._module_file
