import os
from dotenv import load_dotenv
from portcraft.lib._pathlib import Paths, PathUtils

SUPPORTED_EXTENSIONS = [".yaml", "yaml", ".json", ".py"]
CICD_PATH = "./.cicd"
CICD_FILE_NAME = "main.yml"
TMP_DIR = "/tmp/.cicd"
VAR_FILES = ["./vars.yml", "./all.json"]
ENV_FILE = "./.env"
LIBRARY_PATHS = ["portcraft/library"]

def terminal_size() -> int:
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 90  # fixed length

SCREEN_WIDTH = terminal_size()

paths = Paths()
pu = PathUtils(paths.home_path.parent)
all_vars = pu.all_vars
load_dotenv(dotenv_path=paths.env_file)

def env(var) -> str:
    return os.environ.get(var)
