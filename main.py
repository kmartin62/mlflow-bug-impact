# from github import Github
from dotenv import load_dotenv
# from local_git import GitRepo
# import os

load_dotenv()

# TOKEN = os.getenv("GIT_TOKEN")
# REPO_NAME = "kmartin62/mlflow-bug-impact"  

# g = Github(TOKEN)
# repo = g.get_repo(REPO_NAME)

# pull_requests = repo.get_pulls(state="open")

# for pr in pull_requests:
#     print(pr)
#     print(f"PR #{pr.number}: {pr.title}")
#     print(f"Author: {pr.user.login}")
#     print(f"State: {pr.state}")
#     print(f"Commits: {pr.commits}")
#     print(f"Comments: {pr.comments}")

#     for commit in pr.get_commits():
#         print(commit)
#         print(f"Commit: {commit.sha} - {commit.commit.message}")

#     for comment in pr.get_issue_comments():
#         print(f"Comment by {comment.user.login}: {comment.body}")

#     print("-" * 50)

# print(GitRepo().get_latest_commit())

from database.db import get_db
from service.pr_service import store_pr
from service.git_commit_service import store_git_commit
from sqlalchemy.orm import Session

db: Session = next(get_db())

stored_gc = store_git_commit(db, "test_hash1", 6, "kmartin62", "fix: test message", 3, 5, 1)
