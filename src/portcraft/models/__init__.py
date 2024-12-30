class Model:
    def __init__(self, attrs=None):
        self.attrs = attrs

    def _getter(self, attr_name: str):
        if attr_name in self.attrs:
            return self.attrs.get(attr_name)
        return None

    @classmethod
    def prepare_model(cls, *args, **kwargs):
        return cls(*args, **kwargs)

    def __call__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def __str__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"


class Stage(Model):
    @property
    def name(self):
        return self._getter('name')

    @property
    def args(self):
        return self._getter('args')

    @property
    def modules(self):
        return [Module.prepare_model(module) for module in self.args]


class Module(Model):
    def __init__(self, attr):
        super().__init__(attr)
        self._name, self._args = self.argument_extractor()

    def argument_extractor(self):
        if not self.attrs:
            raise ValueError("The 'attrs' dictionary is empty. Cannot extract arguments.")

        extracted_name = (
            next((key for key in self.attrs if key != 'name'), None)
            if 'name' in self.attrs
            else next(iter(self.attrs), None)
        )
        return extracted_name, self.attrs.get(extracted_name)


    @property
    def metadata(self) -> str | None:
        if 'name' in self.attrs:
            return self.attrs.get('name', None)

    @property
    def name(self):
        return self._name

    @property
    def arguments(self):
        return self._args
