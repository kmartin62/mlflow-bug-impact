from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.orm import Session
from github import Github
from local_git import GitRepo
import os
from database.models import PullRequest, PullRequestComment, GitCommit
from database.db import get_db

load_dotenv()

TOKEN = os.getenv("GIT_TOKEN")
REPO_NAME = "kmartin62/mlflow-bug-impact"  

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

pull_requests = repo.get_pulls(state="open")

pr_obj = PullRequest()

db: Session = next(get_db())

for pr in pull_requests: # assume only one pr is present all of the time
    pr_obj.id = pr.number
    pr_obj.title = pr.title
    pr_obj.author = pr.user.login
    pr_obj.state = pr.state
    comments = pr.get_issue_comments()
    pr_obj.comments_count = comments.totalCount

db.add(pr_obj)

db.commit()

for comment in pr.get_issue_comments():
    pr_comm = PullRequestComment()
    pr_comm.pr_id = pr_obj.id
    pr_comm.comment = comment.body
    pr_comm.author = comment.user.login

    db.add(pr_comm)

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

    db.add(gc)

db.commit()

    # print(f"PR #{pr.number}: {pr.title}")
    # print(f"Author: {pr.user.login}")
    # print(f"State: {pr.state}")
    # print(f"Commits: {pr.commits}")
    # print(f"Comments: {pr.comments}")

    # for commit in pr.get_commits():
    #     print(commit)
    #     print(f"Commit: {commit.sha} - {commit.commit.message}")

    # for comment in comments:
    #     print(f"Comment by {comment.user.login}: {comment.body}")

    # print("-" * 50)

# print(GitRepo().get_latest_commit())

# from database.db import get_db
# from service.pr_service import store_pr
# from service.git_commit_service import store_git_commit
# from sqlalchemy.orm import Session

# db: Session = next(get_db())

# stored_gc = store_git_commit(db, "test_hash1", 6, "kmartin62", "fix: test message", 3, 5, 1)
