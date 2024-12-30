from portcraft.lib.abstract_tree.transformers import Transformer
from portcraft.settings import paths
from portcraft.lib.common import find_file_path
module = "gitpy"


def _find_module(module):
    module_paths = []
    for library_path in  paths.library_paths:
        module_path = find_file_path(library_path, module)
        if module_path:
            module_paths.append(module_path)

    if not module_paths:
        raise Exception(f"No module found {module} in {paths.library_paths}")

    return module_paths

_mod = _find_module(module)

new_args = {
    "action": "create",
    "repo": "DockCraft",
    "branch": "master",
    "commit": "No",  # Example: adding a new key
}
path = _mod[0]


searcher = Transformer(path, "Crafter")
new_data = searcher.modify_args(module_args=new_args)
searcher.run_module(new_data)
