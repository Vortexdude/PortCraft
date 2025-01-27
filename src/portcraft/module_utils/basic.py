import json
import sys
from io import StringIO, UnsupportedOperation


class Validator:
    def validate_module_args(self, yaml_args: dict):
        """
        Validate the YAML arguments against the user-defined argument constraints.

        Args:
            yaml_args (dict): A dictionary containing the arguments to validate.

        Raises:
            ValueError: If a type mismatch is detected.
            KeyError: If a required argument is missing in the YAML data.
            Exception: If a required parameter is missing or has an invalid value.
        """

        unsupported_args = [arg for arg in yaml_args.keys() if arg not in self.module_args]
        if unsupported_args:
            raise KeyError(f"Argument: '{unsupported_args}' not supported by the module")

        for key, constrain in self.module_args.items():
            if key not in yaml_args:
                if constrain.get('required', False):
                    raise KeyError(f"Missing required parameter: {key}")
                else:
                    print(f"Optional Argument '{key}' not provided so skipping ... ")
                    continue

            value = yaml_args[key]
            expected_type = constrain['type']
            if expected_type and type(value) != expected_type:
                raise ValueError(f"Type mismatch for parameter '{key}': Expected {expected_type.__name__}, "
                                 f"got {type(value).__name__}")

            if constrain.get('required', False) and not value:
                raise ValueError(f"Parameter '{key}' is required but has no value.")


class Crafter(Validator):
    def __init__(self, module_args=None):
        self.module_args: dict = module_args  # that will be required in yaml
        self.params = self._load_params()
        self.__setup()
        self.result = {}
        self._validate()


    def __setup(self):
        try:
            self.validate_module_args(self.params)
        except ValueError as e:
            print(e)
            sys.exit(13)

    def _validate(self):
        for arg, spec in self.module_args.items():
            if spec.get("required", False) and arg not in self.params:
                self.fail_json(msg=f"Missing required parameter: {arg}")
            if arg in self.params and not isinstance(self.params[arg], spec['type']):
                self.fail_json(msg=f"Invalid type for parameter: {arg}. Expected {spec['type'].__name__}")

    def _load_params(self):
        try:
            raw_data: StringIO = sys.stdin
            raw_data.seek(0)
            json_string = raw_data.read()
            return json.loads(json_string)
        except UnsupportedOperation:
            self.fail_json(msg="Cant run Standalone file need to be by the tool itself", code=256)

        except json.JSONDecodeError:
            self.fail_json(msg="Invalid JSON input")


    def exit(self, kwargs):
        self.result =  kwargs
        sys.exit(0)

    def validate(self): pass

    @staticmethod
    def fail_json(**kwargs):
        msg = kwargs.get('msg', "")
        code = kwargs.get("code", 0)
        print(f"ERROR {code} - > ", msg)
        sys.exit(code)
