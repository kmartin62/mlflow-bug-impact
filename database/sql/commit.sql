CREATE TABLE IF NOT EXISTS git_commit (
	id SERIAL PRIMARY KEY,
  hash TEXT NOT NULL UNIQUE,
  pr_id INTEGER,
  author TEXT NOT NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  lines_added INTEGER NOT NULL DEFAULT 0,
  lines_deleted INTEGER NOT NULL DEFAULT 0,
  affected_files_count INTEGER NOT NULL DEFAULT 0,
  commit_type_id INT REFERENCES commit_type(id),
  CONSTRAINT fk_pr
    FOREIGN KEY (pr_id)
    REFERENCES pull_request(id)
    ON DELETE CASCADE -- this is used for the following thing: delete comment if pr is deleted

);