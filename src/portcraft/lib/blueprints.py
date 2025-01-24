
from yaml import safe_load
from pathlib import Path
from portcraft.settings import paths, env, all_vars
from portcraft.lib.display import colier_console, default_console, minimal_console
from portcraft.lib.parser import _file_parser
from cloudhive.utils import load_yml


file = "test.yml"

home_dir = paths.home_path

class Explorer:
    def __init__(self, data):
        self.data = data

    @classmethod
    def load(cls, file):
        return cls(load_yml(file))

    def get_stages(self) -> dict:
        if 'stages' in self.data:
            return self.data.get('stages', {})

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
        # find the module in the module directory
        # inject the data into the module
        for plugin_name, plugin_args in self._plugins.items():
            print(f"Discovering plugin '{plugin_name}' with arg '{plugin_args}'")

        print(default_console.inject(module_name=self._name, module_comment=self._comment))


class Blueprint:
    """ Represents a detailed plan or script for executing tasks, similar to a "blueprint" for a project. """

    def __init__(self): pass

    def run(self, filename=None):

        filepath = _file_parser(filename)
        explorer = Explorer.load(filepath)
        # loader = explorer.data
        stages = explorer.get_stages()
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


        # if stages:
        #     for stage_name, stage_data in stages.items():
        #         if isinstance(stage_data, list):
        #             for module in stage_data:
        #                 print(module)


            # stages = data['stages']
            # if isinstance(stages, dict):
                # for name, item in stages.items():
                #     print(f"=> STAGE [{name}]")
                #     if isinstance(item, list):
                #         for module in item:
                #             if "name" in module:
                #                 print(f"Comment => {module['name']}")
                #                 del module['name']
                #             module_name, module_data = next(iter(module.items()))
                #             print(module_name, module_data)



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
