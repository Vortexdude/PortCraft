from cloudhive import utils
import requests


class Git(object):
    def __init__(self, url: str, user=None, repo=None):
        self._url = url
        self._user = user
        self._repo = repo
        self._headers = dict()
        self.base_url = "https://api.github.com"
        self.validate()
        self._is_public: bool = True

    def validate(self):
        if not self._url.startswith("https://github.com/"):
            raise Exception("No a github url")

        if self._url.endswith(".git"):
            self._url = self._url[:-4]

        protocol, _, server, self._user, self._repo = self._url.split("/")
        _url = utils.url_joiner(self.base_url, "repos", self._user, self._repo)
        print(f"# => Validating repo {_url}")
        response = requests.get(_url)
        if response.status_code == 404:
            print(f"# => repo {self._user} {self._repo} is not public")
            self._is_public = False

    def __call__(self):
        return f"<Git {self._user}/{self._repo}>"


class GitPy(Git):
    FILE_EXTENSION = ".zip"
    TEMP_FILE_LOCATION = "/tmp/.cicd"
    envs: dict = utils.load_env_vars("GIT_TOKEN")

    def download_public_repo(self, branch=None, download_location=None):
        file_name = f"{branch}.zip"
        url = utils.url_joiner("https://github.com", self._user, self._repo, "archive/refs/heads", file_name)
        print(f"# => Downloading public rep {url=}")
        utils.download_file(url, file_name)
        return file_name


    def download_repo(self, branch=None, pa_token:str=None, download_location=None):

        if not branch:
            branch = "main"

        if not self._is_public:
            if not pa_token:
                pa_token = self.envs.get("GIT_TOKEN")

            if not pa_token:
                raise Exception("please specify the personal access token first")

            self._headers['Authorization'] = f"Bearer {pa_token}"

        if not download_location:
            download_location = self.TEMP_FILE_LOCATION

        utils.create_directory(download_location)
        local_file = utils.path_joiner(download_location, (self._repo + self.FILE_EXTENSION))
        if self._is_public:
            zip_file = self.download_public_repo(branch=branch)

        else:
            self._headers['Accept'] = "application/vnd.github+json"
            download_args = ("repos", self._user, self._repo, "zipball", branch)
            url = utils.url_joiner(self.base_url, *download_args)
            zip_file = utils.download_file(url, local_file, headers=self._headers)
        self.__file_handling(zip_file)


    def __file_handling(self, zip_file):
        # Unzipping files
        ultimate_file = utils.unzip(zip_file, parent_dir=zip_file.parent)

        # move the child directory the similar to `mv .cicd/repo/repo_xyxd123 .cicd/repo1`
        __temp_file = str(utils.path_joiner(self.TEMP_FILE_LOCATION, "repo1"))
        utils.move_files(f"{str(ultimate_file)}/*", __temp_file)

        # cleanup the file
        [utils.cleanup_file(item) for item in [zip_file, ultimate_file]]

        # change the repo1 to the actual name of the repo
        utils.move_files(__temp_file, str(utils.path_joiner(self.TEMP_FILE_LOCATION, ultimate_file.stem)))


gg = GitPy("https://github.com/Vortexdude/DockCraft")
gg.download_repo(branch="master")