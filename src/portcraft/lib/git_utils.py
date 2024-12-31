from cloudhive.utils import url_joiner, path_joiner, load_env_vars, download_file, move_files, cleanup_file, unzip, \
    create_directory
import requests
import os

def url_formatter(base_url, *args) -> str:
    return url_joiner(base_url, *args)

def rename_file(source, dest):
    os.rename(source, dest)


class Git(object):
    def __init__(self, url: str, user=None, repo=None):
        self._url = url
        self._user = user
        self._repo = repo
        self._headers = dict()
        self.git_api_base_url = "https://api.github.com"
        self.git_base_url = "https://github.com"
        self.validate()

    def validate(self):
        if not self._url.startswith("https://github.com/"):
            raise Exception("No a github url")

        if self._url.endswith(".git"):
            self._url = self._url[:-4]

        protocol, _, server, self._user, self._repo = self._url.split("/")

    def _repo_visibility(self) -> bool:

        _url = url_formatter(self.git_api_base_url, "repos", self._user, self._repo)
        response = requests.get(_url)
        if response.status_code == 404:
            print(f"# => repo {self._user} {self._repo} is not public")
            return False
        return True

    @property
    def is_public(self):
        return self._repo_visibility()

    def __call__(self):
        return f"<Git {self._user}/{self._repo}>"


class GitPy(Git):
    FILE_EXTENSION = ".zip"
    TEMP_FILE_LOCATION = "/tmp/.cicd"
    envs: dict = load_env_vars("GIT_TOKEN")

    def download_public_repo(self, branch=None, download_location=None):
        file_name = f"{branch}.zip"
        _url = url_formatter(self.git_base_url, self._user, self._repo, "archive/refs/heads", file_name)
        print(f"# => Downloading public rep with {_url=}")
        download_file(_url, file_name)
        dest_file = f"{self._repo}.zip"
        rename_file(file_name, dest_file)
        return dest_file

    def download_private_repo(self, branch, pa_token=None, local_file=None):
        pa_token = pa_token or self.envs.get("GIT_TOKEN")
        if not pa_token:
            raise Exception("please specify the personal access token first")

        self._headers.update({
            "Authorization": f"Bearer {pa_token}",
            "Accept": "application/vnd.github+json",
        })
        _url = url_formatter(self.git_api_base_url, "repos", self._user, self._repo, "zipball", branch)
        print(f"# => Downloading private repo with URL: {_url=}")

        return download_file(_url, local_file, headers=self._headers)

    def download_repo(self, branch=None, pa_token: str = None, download_location=None):

        branch = branch or "main"
        download_location = download_location or self.TEMP_FILE_LOCATION
        create_directory(download_location)
        local_file = path_joiner(download_location, f"{self._repo}{self.FILE_EXTENSION}")  # /tmp/.cicd/repo.zip
        if self.is_public:
            zip_file = self.download_public_repo(branch=branch)
        else:
            zip_file = self.download_private_repo(branch=branch, pa_token=pa_token, local_file=local_file)

        self.__file_handling(zip_file)

    def __file_handling(self, zip_file):
        # Unzipping files
        ultimate_file = unzip(zip_file)

        # move the child directory the similar to `mv .cicd/repo/repo_xyxd123 .cicd/repo1`
        temp_repo_dir = str(path_joiner(self.TEMP_FILE_LOCATION, "repo_temp"))
        move_files(f"{str(ultimate_file)}/*", temp_repo_dir)

        # cleanup the file
        [cleanup_file(item) for item in [zip_file, ultimate_file]]

        # change the repo1 to the actual name of the repo
        move_files(temp_repo_dir, str(path_joiner(self.TEMP_FILE_LOCATION, ultimate_file.stem)))


# gg = GitPy("https://github.com/Vortexdude/dockcraft")
# gg.download_repo(branch="master")
