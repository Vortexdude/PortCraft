"""
PORTCRAFT a Custom CICD tool
that's configuration is defined in the yaml file
"""

from cloudhive import utils
from portcraft.models import Stage, Module
from portcraft.settings import paths
from portcraft.lib.common import find_module_path
from portcraft.lib.abstract_tree.transformers import Transformer

class Extractor(object):
    def __init__(self, config):
        self.__conf = config
        self._stages = self._extract('stages')

    def _extract(self, name: str):
        if isinstance(self.__conf, dict) and name in self.__conf:
            return self.__conf[name]
        elif isinstance(self.__conf, list):
            return self.__conf[0][name]
        return []

    @property
    def stages(self):
        return [Stage.prepare_model(attrs={"name": name, "args": value}) for name, value in self._stages.items()]


class Crafter(Extractor):

    def run(self):
        for stage in self.stages:
            print(f"=> Inside {stage.name}")
            for module in stage.modules:
                print(f"=> Running {module.name}")
                self.stage_runner(module)


    @staticmethod
    def stage_runner(module: Module):
        module_path = find_module_path(module.name.lower())[0]
        trs_obj = Transformer(module_path, "Crafter")
        module_data = trs_obj.modify_args(kwargs=module.arguments)
        trs_obj.run_module(module_data)


def main(config):
    craft = Crafter(config)
    craft.run()


if __name__ == "__main__":

    data = utils.load_yml(paths.cicd_file)
    if not data:
        raise Exception("Cant find the config file.")

    main(data)

