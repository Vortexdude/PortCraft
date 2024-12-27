from src.lib.abstract_tree.transformers import Transformer


new_args = {
    "action": "create",
    "repo": "DockCraft",
    "branch": "master",
    "commit": "No",  # Example: adding a new key
}

searcher = Transformer("GitPy.py", "Crafter")
new_data = searcher.modify_args(module_args=new_args)
searcher.run_module(new_data)
