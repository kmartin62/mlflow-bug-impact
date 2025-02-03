CREATE TABLE IF NOT EXISTS pull_request (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	author TEXT NOT NULL,
  state VARCHAR(10) CHECK (state IN ('open', 'closed', 'merged')),
  comments_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  merged_at TIMESTAMP
);