from pathlib import Path

CICD_PATH = "./.cicd"
CICD_FILE_NAME = "main.yml"
TMP_DIR = "/tmp/.cicd"
LIBRARY_PATHS = ["portcraft/library"]


class Paths:
    def __init__(self, home_dir: Path=None):
        if not home_dir:
            home_dir = Path(__file__).parent

        self._home_path = home_dir
        self._cicd_file = self._home_path / CICD_PATH / CICD_FILE_NAME
        self._library_paths = [self._home_path.parent / path for path in LIBRARY_PATHS]

    @property
    def home_path(self):
        return self._home_path

    @property
    def cicd_file(self):
        for item in [self._home_path, self.home_path.parent.parent]:
            path = item / CICD_PATH / CICD_FILE_NAME
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

paths = Paths()
