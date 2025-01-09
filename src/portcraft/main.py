"""
PORTCRAFT a Custom CICD tool
that's configuration is defined in the yaml file
"""

from cloudhive import utils
from portcraft.settings import paths
from portcraft.lib.display import Console
from portcraft.lib.common import find_module_path
from portcraft.lib.abstract_tree.extractors import Extractor
from portcraft.lib.abstract_tree.transformers import Transformer

console = Console()


class Crafter(Extractor):
    """
    Orchestrates the execution of stages and modules defined in the configuration.
    """
    def run(self):
        """
        Execute all stages and their modules.
        """
        for stage in self.stages:
            console.stage_bar(stage.name)
            for module in stage.modules:
                if module.register:
                    print("Saving the data to the variable . . .")
                console.task_bar(module)
                self.stage_runner(module)


    @staticmethod
    def stage_runner(module):
        module_path = find_module_path(module.name.lower())[0]
        transformer = Transformer(module_path, "Crafter")
        modified_ast = transformer.modify_args(kwargs=module.arguments)
        transformer.run_module(modified_ast)


def main(config):
    """
    Main function to initialize and run the Crafter with the given configuration.

    Args:
        config (dict): Configuration data.
    """
    craft = Crafter(config)
    craft.run()


if __name__ == "__main__":
    # Load the configuration file
    config_data = utils.load_yml(paths.cicd_file)
    if not config_data:
        raise FileNotFoundError("Cannot find the config file.")

    # Execute the main function
    main(config_data)
