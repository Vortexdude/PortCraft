from portcraft.lib.abstract_tree.transformers import Transformer
from portcraft.settings import paths
print(paths.home_path)

new_args = {
    "action": "create",
    "repo": "DockCraft",
    "branch": "master",
    "commit": "No",  # Example: adding a new key
}
path = "portcraft/library/GitPy.py"


# searcher = Transformer(path, "Crafter")
# new_data = searcher.modify_args(module_args=new_args)
# searcher.run_module(new_data)
