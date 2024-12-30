class Crafter(object):
    def __init__(self, module_args=None):
        self.module_args: dict = module_args # that will be required in yaml
        print(f"{self.module_args=}")
        self._params = None

    @property
    def params(self):
        return self._params

    @staticmethod
    def exit(**kwargs):
        if 'message' in kwargs:
            return kwargs['message']
