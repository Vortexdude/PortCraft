import os
from cloudhive.utils import basename, url_joiner
from portcraft.settings import paths


def find_module_path(module):
    module_paths = []
    for library_path in  paths.library_paths:
        module_path = find_file_path(library_path, module)
        if module_path:
            module_paths.append(module_path)

    if not module_paths:
        raise Exception(f"No module found {module} in {paths.library_paths}")

    return module_paths


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
