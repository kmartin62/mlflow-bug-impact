CREATE TABLE IF NOT EXISTS pull_request (
	id PRIMARY KEY,
	title VARCHAR(20) UNIQUE NOT NULL,
	author VARCHAR(20) UNIQUE NOT NULL,
  state VARCHAR(10) CHECK (state IN ('open', 'closed', 'merged')),
  comments_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  merged_at TIMESTAMP
);