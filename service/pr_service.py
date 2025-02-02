from database.models import PullRequest
from sqlalchemy.orm import Session

def store_pr(db: Session, 
             pr_number, 
             title, 
             author, 
             state, 
             comments_count,
            #  created_at,
            #  merged_at
             ):
  pr = PullRequest(
    id = pr_number,
    title = title,
    author = author,
    state = state,
    comments_count = comments_count,
    # created_at = created_at,
    # merged_at = merged_at
  )
  db.add(pr)
  db.commit()
  return pr