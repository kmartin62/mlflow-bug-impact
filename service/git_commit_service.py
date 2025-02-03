from database.models import GitCommit
from sqlalchemy.orm import Session

def store_git_commit(db: Session, 
                     hash, 
                     pr_id, 
                     author, 
                     message, 
                     lines_added,
                     lines_deleted,
                     affected_files_count
                     ):
  pr = GitCommit(
    hash = hash,
    pr_id = pr_id,
    author = author,
    message = message,
    lines_added = lines_added,
    lines_deleted = lines_deleted,
    affected_files_count = affected_files_count
  )
  db.add(pr)
  db.commit()
  return pr