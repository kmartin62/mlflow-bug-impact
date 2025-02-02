CREATE TABLE pull_request_comments (
  id SERIAL PRIMARY KEY,
  pr_id INTEGER NOT NULL,
  comment TEXT NOT NULL,
  author TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_pr_comment
    FOREIGN KEY (pr_id)
    REFERENCES pull_request(id)
    ON DELETE CASCADE -- this is used for the following thing: delete comment if pr is deleted
)