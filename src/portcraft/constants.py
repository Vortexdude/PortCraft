import requests
import os


_GIT_DEFAULT_BRANCH = "main"
_GIT_API_BASE_URL = "https://api.github.com"

# res = requests.get("https://api.github.com/repos/Vortexdude/DockCraft")









class ConfigManager(object):
    def __init__(self, conf_file=None):
        self._conf_file = conf_file

    data = "%s/base.yml" % os.path.dirname(__file__)
