from dotenv import load_dotenv
import os
load_dotenv()
# from transformers import pipeline
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import PullRequestCommentSentiment

db: Session = next(get_db())

db.add(PullRequestCommentSentiment(
    pr_id=3,
    sentiment_label="positive",
    confidence=0.92,
))
db.commit()
# sms = SentimentModelService()
# model = sms.get(db)
# os.environ["ACTIVE_SENTIMENT_MODEL"] = model # cache it, fetch only 1st time from the database; TODO: maybe this can be added somewhere else? Redefine after finishing main.py functions for each segment

# print(model)

# # model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
# sentiment_pipeline = pipeline("text-classification", model=model)
# comments = ["Great job!", "This code is terrible.", "Needs some improvements."]

# results = sentiment_pipeline(comments)
# print(results)
# from dotenv import load_dotenv
# load_dotenv()
# # TODO: add rollback, clear code
# from sqlalchemy.orm import Session
# from github import Github
# from local_git import GitRepo
# import os
# from database.models import PullRequest
# from database.db import get_db
# from service import PullRequestService, PullRequestCommentsService

# # pr_service = PullRequestService()
# pr_service = PullRequestCommentsService()
# db: Session = next(get_db())
# print(pr_service.get_by_id(db, 3)[1].comment)

# TOKEN = os.getenv("GIT_TOKEN")
# REPO_NAME = "kmartin62/mlflow-bug-impact"  

# g = Github(TOKEN)
# repo = g.get_repo(REPO_NAME)

# pull_requests = repo.get_pulls(state="open")

# pr_obj = PullRequest()

# db: Session = next(get_db())

# for pr in pull_requests: # assume only one pr is present all of the time
#     pr_obj.id = pr.number
#     pr_obj.title = pr.title
#     pr_obj.author = pr.user.login
#     pr_obj.state = pr.state
#     comments = pr.get_issue_comments()
#     pr_obj.comments_count = comments.totalCount

# db.add(pr_obj)

# db.commit()

# for comment in pr.get_issue_comments():
#     pr_comm = PullRequestComment()
#     pr_comm.pr_id = pr_obj.id
#     pr_comm.comment = comment.body
#     pr_comm.author = comment.user.login

#     db.add(pr_comm)

# for commit in pr.get_commits():
#     gc = GitCommit()
#     gc.hash = commit.sha
#     gc.pr_id = pr_obj.id
#     gc.author = commit.author.login if commit.author else "N/A"
#     gc.message = commit.commit.message
#     gc.created_at = commit.commit.committer.date
#     gc.lines_added = commit.stats.additions
#     gc.lines_deleted = commit.stats.deletions
#     gc.affected_files_count = commit.files.totalCount

#     db.add(gc)

# db.commit()

