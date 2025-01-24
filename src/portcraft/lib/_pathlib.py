import os
from typing import Optional, Dict
from pathlib import Path
from cloudhive.utils import load_config

__all__ = ["Paths", "PathUtils"]


def extract_data(files) -> Dict:
    """
    Extracts data from the identified variable files.

    Returns:
        Dict: A dictionary containing aggregated data from all matching files.
    """
    data = {}
    for file in files:
        data.update(load_config(str(file)))
    return data


class Paths:
    def __init__(self, home_dir: Optional[Path] = None):
        """
        Initializes the Paths class.
        Args:
            home_dir (Optional[Path]): The root directory to set as the home path.
            Defaults to the parent directory of the current file.
        """

        if not home_dir:
            home_dir = Path(__file__).parent

        self._home_path = home_dir
        self._cicd_file = self._home_path / "./.cicd/main.yml"
        self._library_paths = [self._home_path.parent / path for path in  ["portcraft/library"]]
        self.env_file = self._home_path / "./.env"

    @property
    def home_path(self) -> Path:
        """Returns the home directory path."""
        return self._home_path

    @property
    def cicd_file(self) -> Path | None:
        """Finds and returns the CICD file path if it exists."""

        for item in [self._home_path, self.home_path.parent.parent]:
            path = item / "./../.cicd/main.yml"

            if path.exists():
                return path
        return None

    @property
    def library_paths(self):
        return self._library_paths

    def lib_extractor(self):
        __lib_path = []
        for lib_path in self._library_paths:
            _lib_path = str(lib_path).split(str(self._home_path))[1]
            if str(lib_path).startswith("/"):
                lib_path = _lib_path[1:].replace("/", ".")
            __lib_path.append(lib_path)
        return __lib_path


class PathUtils:
    """
    A utility class to handle file searching and data extraction from a specified directory.

    Attributes:
        home_dir (Path): The root directory to search for files.
        var_files (List[str]): A list of file paths matching the specified criteria.
        all_vars (Dict): A dictionary containing data extracted from the matching files.
    """

    def __init__(self, home_dir: Path):
        self.home_dir = Path(home_dir) if not isinstance(home_dir, Path) else home_dir
        self.var_files = list(self.find_var_files())
        self.all_vars = extract_data(self.var_files)

    def find_var_files(self):
        """
        Finds files in the home directory with specific extensions and criteria.

        Yields:
            Union[str, Path]: Paths of files matching the specified criteria.
        """

        __files = []
        valid_extensions = {".py", ".json", ".yaml", ".yml"}
        for root, _, files in os.walk(self.home_dir):
            for file in files:
                if (
                        file.endswith(tuple(valid_extensions))
                        and file != "__init__.py"
                        and not file.endswith(".pyc")
                        and "all" in file
                ):
                    yield Path(root) / file
