import sys
from portcraft.constants import task_display_mapping
from cloudhive.display.console import ConsoleFormatter

cs = ConsoleFormatter(task_display_mapping)
default_console = cs.Trooper("default")
colier_console = cs.Trooper("colier")
minimal_console = cs.Trooper("minimal")

def console(data: str):
    _buff_char = ""
    if not data.startswith("\r"):
        _buff_char += "\r"
    if "033[K" not in data:
        _buff_char += "\033[K"

    sys.stdout.write(_buff_char + data)
    sys.stdout.flush()
