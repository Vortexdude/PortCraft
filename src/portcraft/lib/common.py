import os

from cloudhive.utils import basename, url_joiner

def find_file_path(_lib_path, module):
    for file in _lib_path.glob("*"):
        if ".py" not in module:
            module = f"{module}.py"

        if basename(file).lower() == module:
            return file
    return []

def url_formatter(base_url, *args) -> str:
    return url_joiner(base_url, *args)

def rename_file(source, dest):
    os.rename(source, dest)
