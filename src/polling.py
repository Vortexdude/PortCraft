# clone the github repo with the branch that need to be cloned
from .git_ops import GitPy














def clone_repo():
    gg = GitPy("https://github.com/Vortexdude/DockCraft")
    gg.download_repo(branch="master")

def check_pass():
    pass

def crete_docker_container(image, repo_url):
    clone_repo(repo_url)
    run_scipt()


