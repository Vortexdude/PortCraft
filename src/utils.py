import importlib
from .settings import paths

def import_module(_mod, search_paths:list=None):
    """
    Dynamically imports a module and retrieves a class or attribute.

    Args:
        _mod (str): The name of the class or attribute to import.

        search_paths (list): list of the paths.

    Returns:
        Any: The imported class or attribute, or None if not found.
    """
    if not search_paths:
        search_paths = paths.library_paths

    for library_path in search_paths:
        try:
            module = importlib.import_module(library_path)
            if hasattr(module, _mod):
                return getattr(module, _mod)

        except ImportError:
            print(f"Failed to import module '{library_path}'. Skipping...")

        except AttributeError:
            print(f"'{_mod}' not found in '{library_path}'. Skipping...")

    print(f"'{_mod}' could not be found in any of the provided library paths.")
    return None

