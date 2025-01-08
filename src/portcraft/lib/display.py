from portcraft.settings import SCREEN_WIDTH
from portcraft.models import Module
from portcraft.constants import chars


def task_bar(module_name, module_metadata=None) -> str:
    _output = f"\nMODULE [{module_name}] "
    if module_metadata:
        _output += f"{module_metadata} "

    remaining_dots = SCREEN_WIDTH - 15 - len(module_metadata or "") - len(module_name)
    _output += "." * max(remaining_dots, 0)
    return _output


def task_console(module: Module) -> str:
    """
    Generate console output for a module.

    Args:
        module (Module): The module object to display.

    Returns:
        str: Formatted console string for the module.
    """
    output = task_bar(module.name, module.metadata)
    print(output)



def stage_bar(stage: str) -> str:
    """
    Print the State Grafity
    it will automatically convert from lower case to uppercase
    Args:
        stage (str): The text to display.

    Returns:
        str: Formatted console string for the module.
    """
    # convert the text to upper case
    text = stage.upper()

    # convert text to list
    b=list(map(str, text))

    # get the ASCII ART value of the character and split it with "/n"
    char_lists = [chars[item].split("\n") for item in b]

    # merge the first each first line with each character and add new line character at the end
    result = "\n".join(["  ".join(elements) for elements in zip(*char_lists)])
    return result + "\n"
