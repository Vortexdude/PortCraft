import sys
from portcraft.lib.display import default_console
from portcraft.lib.parser import _file_parser
from cloudhive.utils import load_yml
from portcraft.lib.packer import TaskPacker

from portcraft.models import Module

def banner(*args, **kwargs):
    main = """
-------------------------------------------------------
    Portcraft - Lightweight CI/CD Container Runner
-------------------------------------------------------

    [FEATURES]
    - 🐳 Runs commands inside Docker containers
    - 🚀 Automates your builds, tests, and deployments
    - 🛠️  Portable, reliable, and easy to use

    [WORKFLOW]
    -> Input Command ➡️ Container Execution ➡️ Logs & Results
-------------------------------------------------------
"""
    print(main)


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
        stage_data = None
        if isinstance(self.data, list) and self.data:
            stage_data = self.data[0].get('stages', {})
        elif isinstance(self.data, dict):
            stage_data = self.data.get('stages', {})

        # Update the internal stages dictionary if data exists
        if stage_data:
            self.__stages.update(stage_data)


class Blueprint:
    """ Represents a detailed plan or script for executing tasks, similar to a "blueprint" for a project. """

    def __init__(self, filename=None, debug=None, ignore_errors=None, dry_run=None):
        banner()
        self._filename = filename or "test.yml"
        self._debug: bool = debug or False
        self._ignore_errors: bool = ignore_errors or False
        self._dry_run = dry_run or False

    def run(self, filename=None):
        filename = filename or self._filename
        filepath = _file_parser(filename)
        explorer = Explorer.load(filepath)
        stages = explorer.stages
        for stage_name, stage_data in stages.items():
            if not stage_data:
                raise ValueError(f"No Task are defined in the stage '{stage_name}'") # you can exit and for dy run just ignore this

            print(f"running {stage_name}")
            for module in stage_data:
                mk = Module(module)
                task = TaskPacker(
                    module_name=mk.name,
                    module_args=mk.args,
                    module_plugins=mk.plugins,
                    context=self,
                    module_comment=mk.comment,
                )
                print("\n"+ default_console.inject(module_name=mk.name, module_comment=mk.comment))
                code = task.run()
                if code >= 1 and not self._ignore_errors:
                    sys.exit(1)

    # @staticmethod
    # def template_render(file: Path):
    #     from jinja2 import Environment, FileSystemLoader
    #     environment = Environment(loader=FileSystemLoader(file.parent.resolve()))
    #     template = environment.get_template(file.name)
    #     content = template.render(**all_vars)
    #     data = safe_load(content)


# args = dict(
#     filename="test.yml",
#     debug=False,
#     ignore_errors=True,
# )
# Blueprint(**args).run()
