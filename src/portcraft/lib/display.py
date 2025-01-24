from portcraft.constants import task_display_mapping
from cloudhive.display.console import ConsoleFormatter

cs = ConsoleFormatter(task_display_mapping)
default_console = cs.Trooper("default")
colier_console = cs.Trooper("colier")
minimal_console = cs.Trooper("minimal")
