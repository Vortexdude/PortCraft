import sys
import time
from portcraft.lib.blueprints import Blueprint

# _file = "test.yml"

# bp = Blueprint(filename=_file)
# bp.run()






def is_odd(data: int | str):
    if isinstance(data, str):
        data = len(data)
    if data % 2:
        return True
    return False


def generate_banner(title, width=None):
    if not width:
        width = 50
    _banner = ""
    title_length = len(title)
    if title_length >= width:
        width = (title_length + 10)

    _is_width_odd = is_odd(width)
    _is_title_odd = is_odd(title_length)
    _face_border = f"+{'-' * (width - 2)}+\n"
    _banner += _face_border
    if _is_title_odd and not _is_width_odd:
        title += " "
    if not _is_title_odd and _is_width_odd:
        title += " "

    _padding = (width - len(title)) // 2 - 1
    _middle_section = f"|{' ' * _padding}{title}{' ' * _padding}|\n"
    _banner += _middle_section
    _banner += _face_border
    return _banner





def generate_line(text, width=None):
    if not width:
        width = 50
    _text_size = len(text)
    pass


MAX_WIDTH = 80
banner = generate_banner("PORTCRAFT RUN SUMMARY", width=MAX_WIDTH)
pri(banner)

# for item in ["gitpy", "remoterun", "bash"]:
#     pri(generate_line(f"{PROC_START} Module: {item}: Started", width=MAX_WIDTH))
#     time.sleep(0.5)
#     pri(generate_line(f"{PROC_PROGRESS} Module: {item}: running", width=MAX_WIDTH))
#     time.sleep(0.5)
#     pri(generate_line(f"{PROC_ERROR} Module: {item}: error", width=MAX_WIDTH))
#     time.sleep(0.5)
#     print()
line = f"{PROC_START} Module: GitPY: Started"
print(line.center(80, " "))
