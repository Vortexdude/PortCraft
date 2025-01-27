import importlib
import json

from yaml import safe_load
from pathlib import Path
from portcraft.settings import paths, env, all_vars, pu
from portcraft.lib.display import default_console
from portcraft.lib.parser import _file_parser
from cloudhive.utils import load_yml

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
    m_spec.loader.exec_module(module)
    return module


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


file = "test.yml"


class Explorer:
    def __init__(self, data):
        """
        Initialize the Explorer with the provided data.

        :param data: A dictionary or list containing the configuration data.
        """
        self.data = data
        self.__stages = {}
        self.__parse_stages()

    @classmethod
    def load(cls, file: str):
        """
        Load data from a YAML file and initialize the Explorer.

        :param file: Path to the YAML file.
        :return: An instance of Explorer initialized with the loaded data.
        """
        return cls(load_yml(file))

    @property
    def stages(self) -> dict:
        """
        Get the stages data parsed from the input.

        :return: A dictionary of stages.
        """
        return self.__stages

    def __parse_stages(self):
        if isinstance(self.data, list) and self.data:
            stage_data = self.data[0].get('stages', {})
        elif isinstance(self.data, dict):
            stage_data = self.data.get('stages', {})

        # Update the internal stages dictionary if data exists
        if stage_data:
            self.__stages.update(stage_data)


class Module:
    def __init__(self, attrs):
        self._attrs = attrs
        self._name = None
        self._comment = None
        self._module_args = {}
        self._plugins = {}
        self.format()

    def format(self):
        for key, value in self._attrs.items():
            if key == "name": # grab the comment if possible
                self._comment = value
            elif isinstance(value, dict): # check for the args for the module
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


class TaskPacker:
    def __init__(self, module_name, module_args, module_plugins: dict=None, vars=None, module_comment=None):
        self._name = module_name
        self._args = module_args
        self._plugins = module_plugins
        self._vars = vars
        self._comment = module_comment


    def run(self):
        for plugin_name, plugin_args in self._plugins.items():
            print(f"Discovering plugin '{plugin_name}' with arg '{plugin_args}'")

        print(default_console.inject(module_name=self._name, module_comment=self._comment))
        load_and_run_module(self._name, data=self._args)


class Blueprint:
    """ Represents a detailed plan or script for executing tasks, similar to a "blueprint" for a project. """

    def __init__(self): pass

    def run(self, filename=None):

        filepath = _file_parser(filename)
        explorer = Explorer.load(filepath)
        # loader = explorer.data
        stages = explorer.stages
        for stage_name, stage_data in stages.items():
            print(f"running {stage_name}")
            for module in stage_data:
                mk = Module(module)
                task = TaskPacker(
                    module_name=mk.name,
                    module_args=mk.args,
                    module_plugins=mk.plugins,
                    vars=None,
                    module_comment=mk.comment
                )
                task.run()



    @staticmethod
    def template_render(file: Path):
        from jinja2 import Environment, FileSystemLoader
        environment = Environment(loader=FileSystemLoader(file.parent.resolve()))
        template = environment.get_template(file.name)
        content = template.render(**all_vars)
        data = safe_load(content)



        # extract the content in loader object
        # loop through the list
        # evaluate the template
        # create the context for the item
        # pack the additional values like Extensions, comments, variables, hosts
        # Execute every task or command


ss = Blueprint().run("test.yml")
