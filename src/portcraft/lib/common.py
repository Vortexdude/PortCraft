from cloudhive.utils import basename

def find_file_path(_lib_path, module):
    for file in _lib_path.glob("*"):
        if ".py" not in module:
            module = f"{module}.py"

        if basename(file).lower() == module:
            return file
    return []
