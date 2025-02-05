from database.models.git_commit import GitCommit
from database.models.pull_request import PullRequest
from database.models.pull_request_comment import PullRequestComment
from git import Repo
from github import Github

from service.pr_service import PullRequestService

class GitRepoDefinition:
  def __init__(self, token, repo_name, db):
    self.token = token
    self.repo_name = repo_name
    self.db = db

    self.git_repo = Repo()
    self.g = Github(self.token)
    self.repo = self.g.get_repo(self.repo_name)
    self.pull_requests = self.repo.get_pulls(state="open")

    self.pr_service = PullRequestService()

  def get_latest_commit(self):
    return self.git_repo.head.commit
  
  def add_to_db(self):
    pr_obj = PullRequest()
    for pr in self.pull_requests:
      self.pr = pr
      pr_obj.id = pr.number
      pr_obj.title = pr.title
      pr_obj.author = pr.user.login
      pr_obj.state = pr.state
      comments = pr.get_issue_comments()
      pr_obj.comments_count = comments.totalCount
    self.pr_service.add(self.db, pr_obj)

    for comment in pr.get_issue_comments():
      pr_comm = PullRequestComment()
      pr_comm.pr_id = pr_obj.id
      pr_comm.comment = comment.body
      pr_comm.author = comment.user.login
      self.db.add(pr_comm)

    for commit in pr.get_commits():
      gc = GitCommit()
      gc.hash = commit.sha
      gc.pr_id = pr_obj.id
      gc.author = commit.author.login if commit.author else "N/A"
      gc.message = commit.commit.message
      gc.created_at = commit.commit.committer.date
      gc.lines_added = commit.stats.additions
      gc.lines_deleted = commit.stats.deletions
      gc.affected_files_count = commit.files.totalCount
  
      self.db.add(gc)