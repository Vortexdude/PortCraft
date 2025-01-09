from portcraft.settings import SCREEN_WIDTH
from portcraft.models import Module
from portcraft.constants import chars, task_display_mapping
from string import Template

class BaseStringTemplate(Template):
    delimiter = "$" # you can overwrite for use the different delimiter

    def safe_loads(self, mapping=None, **kwargs):
        """
        Perform substitution, using a default value for missing placeholders.

        Args:
            mapping (dict, optional): A dictionary with values for substitution.
            **kwargs: Additional keyword arguments for substitution.

        Returns:
            str: The resulting string after substitution.
        """
        if mapping is None:
            mapping = {}

        combine_dict = {**mapping, **kwargs}

        # create a defaultdict for pass the missing key in the format
        class DefaultDict(dict):
            def __missing__(self, key):
                # return f"<{key}>"
                return ""

        safe_mappings = DefaultDict(combine_dict)
        return self.safe_substitute(safe_mappings)


class ConsoleFormatter:
    def  __init__(self):
        self.module_style: str = 'default'
        self.number_of_dots: int = (SCREEN_WIDTH - 20) or 30
        self.chars = chars

    def _task_formatter(self, module_name, module_comment, style=None):

        def total_dots(char="*"):
            return char * (self.number_of_dots - len(module_comment or "") - len(module_name))

        style = self.module_style if not style else style
        unformatted_style = task_display_mapping.get(style)
        injected_data = dict(
            module_name=module_name,
            module_comment=module_comment,
            filler=total_dots()
        )
        formatted_text = BaseStringTemplate(unformatted_style).safe_loads(injected_data)

        return formatted_text

    def _stage_formatter(self, name):
        # convert the text to upper case
        text = name.upper()

        # convert text to list
        b = list(map(str, text))

        # get the ASCII ART value of the character and split it with "/n"
        char_lists = [self.chars[item].split("\n") for item in b]

        # merge the first each first line with each character and add new line character at the end
        result = "\n".join(["  ".join(elements) for elements in zip(*char_lists)])
        return result + "\n"


class Console(ConsoleFormatter):

    def task_bar(self, module: Module, style=None):
        print(super()._task_formatter(module.name, module.metadata, style))

    def stage_bar(self, name):
        print(super()._stage_formatter(name))
