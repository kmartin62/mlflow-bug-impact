# from dotenv import load_dotenv
# load_dotenv()
# import os

# from util.repo import GitRepoDefinition
# from sqlalchemy.exc import SQLAlchemyError
# # from transformers import pipeline
# from sqlalchemy.orm import Session
# from database.db import get_db
# from database.models import MlflowMetrics

# db: Session = next(get_db())

# TOKEN = os.getenv("GIT_TOKEN")
# REPO_NAME = "kmartin62/mlflow-bug-impact"  
# git = GitRepoDefinition(TOKEN, REPO_NAME, db)
# try:
#   git.add_to_db()
#   # db.commit()
# except SQLAlchemyError as e:
#     db.rollback()
# finally:
#     db.close()

# git_hash = "5c8bcd3cfa519e4455036422c0c11b0b8cd3d6e2"

# new_metric = MlflowMetrics(
#     experiment_id="1234541246",
#     run_id="abcdef413411212332424",
#     model="XGBoost",
#     accuracy=0.349,
#     recall=0.72,
#     precision=0.78,
#     f1_score=0.75,
#     roc_auc=0.81,
#     log_loss=0.43,
#     mongo_id="te4124st",
#     commit_hash=git_hash
# )
# db.add(new_metric)
# db.commit()

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

db: Session = next(get_db())
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
    db.rollback()
finally:
    db.close()

