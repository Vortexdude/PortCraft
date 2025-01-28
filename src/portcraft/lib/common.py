import os
from cloudhive.utils import url_joiner
from portcraft.settings import pu


def search_file(_dir, file):
    _file_path = os.path.join(_dir, file)
    if os.path.isfile(_file_path):
        return _file_path
    return False


def find_module_file(mod_name: str, search_path=None):
    if not search_path:
        search_path = pu.library_paths

    for item in search_path:
        _full_path = search_file(item, f"{mod_name}.py")
        if _full_path:
            return _full_path
    return None


def url_formatter(base_url, *args) -> str:
    return url_joiner(base_url, *args)


def rename_file(source, dest):
    os.rename(source, dest)
