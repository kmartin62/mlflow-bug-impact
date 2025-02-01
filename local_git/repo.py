from git import Repo

class GitRepo:
  def __init__(self):
    self.repo = Repo()

  def get_latest_commit(self):
    return self.repo.head.commit