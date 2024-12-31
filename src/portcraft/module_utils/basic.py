import sys

class Crafter(object):
    def __init__(self, module_args=None, params=None):
        self.module_args: dict = module_args # that will be required in yaml
        self.params = params


    @staticmethod
    def exit(**kwargs):
        print(kwargs)
        sys.exit(0)
