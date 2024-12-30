"""
PORTCRAFT a Custom CICD tool
that's configuration is defined in the yaml file
"""
import os
import importlib
import sys
from importlib.machinery import SourceFileLoader
from cloudhive import utils
from src.models import Module, Stage
from src.utils import import_module
from src.settings import paths


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
                ModuleClass = import_module(module.name)
                # ModuleClass(module.arguments)



def main(config):
    # craft = Extractor(config)
    craft = Crafter(config)
    craft.run()


class ModuleRunner:
    def __init__(self, lib_dir):
        self.lib_dir = lib_dir

    def get_python_files(self):
        return [f for f in os.listdir(self.lib_dir) if f.endswith(".py") and f != "__init__.py"]


    def import_module(self, file_path):
        module_name = os.path.splitext(os.path.basename(file_path))[0]
        loader = SourceFileLoader(module_name, file_path)
        spec = importlib.util.spec_from_loader(module_name, loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        print(module.__dict__)
        # module.main()

    def run(self):
        for file in self.get_python_files():
            filepath = os.path.join(self.lib_dir, file)
            try:
                self.import_module(filepath)
            except:
                continue



if __name__ == "__main__":

    # data = utils.load_yml(paths.cicd_file)
    # main(data)
    search_path = paths._library_paths[0]
    ModuleRunner(search_path).run()
