from transformers import pipeline
from dotenv import load_dotenv
load_dotenv()
from database.models.pull_request_comment_sentiment import PullRequestCommentSentiment
from database.models.sentiment_analysis import SentimentModel
from database.models.git_commit import GitCommit
from database.models.pull_request_comment import PullRequestComment

# TODO: clear code
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from github import Github
import os
from database.models import PullRequest
from database.db import get_db


def get_active_sentiment_model(db: Session):
    model = db.query(SentimentModel).filter_by(is_active=True).first()
    return model.sentiment_analysis_model if model else os.getenv("DEFAULT_SENTIMENT_MODEL")

db: Session = next(get_db())

# cache in case for an api and dont re-read from db every call
model_name = get_active_sentiment_model(db)
os.environ["ACTIVE_SENTIMENT_MODEL"] = model_name

TOKEN = os.getenv("GIT_TOKEN")
REPO_NAME = "kmartin62/mlflow-bug-impact"  

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

pull_requests = repo.get_pulls(state="open")

pr_obj = PullRequest()

try:
    pr_comments = list()
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
        pr_comments.append(comment.body)
        db.add(pr_comm)
    db.commit()

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

    sentiment_pipeline = pipeline("text-classification", model=os.environ['ACTIVE_SENTIMENT_MODEL'])
    pr_text = " ".join(pr_comments)
    result = sentiment_pipeline(pr_text)

    prcs = PullRequestCommentSentiment(
        pr_id = pr_obj.id,
        sentiment_label = result[0].get('label') if len(result) > 0 else 'N/A',
        confidence = result[0].get('score') if len(result) > 0 else 'N/A',
    )
    db.add(prcs)

    db.commit()
except SQLAlchemyError as e:
    print(e)
    db.rollback()
finally:
    db.close()

