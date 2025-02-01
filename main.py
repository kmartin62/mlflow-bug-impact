from github import Github
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("GIT_TOKEN")
REPO_NAME = "kmartin62/mlflow-bug-impact"  

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

pull_requests = repo.get_pulls(state="open")

for pr in pull_requests:
    print(f"PR #{pr.number}: {pr.title}")
    print(f"Author: {pr.user.login}")
    print(f"State: {pr.state}")
    print(f"Commits: {pr.commits}")
    print(f"Comments: {pr.comments}")

    for commit in pr.get_commits():
        print(f"Commit: {commit.sha} - {commit.commit.message}")

    for comment in pr.get_review_comments():
        print(f"Comment by {comment.user.login}: {comment.body}")

    print("-" * 50)