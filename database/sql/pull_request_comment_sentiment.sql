CREATE TABLE IF NOT EXISTS pull_request_comment_sentiment (
    id SERIAL PRIMARY KEY,
    pr_id INTEGER UNIQUE NOT NULL,
    sentiment_label TEXT NOT NULL, 
    confidence FLOAT NOT NULL, 
    analyzed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    model_id INTEGER NOT NULL REFERENCES sentiment_models(id),
    CONSTRAINT fk_pr_comment_sentiment
      FOREIGN KEY (pr_id)
      REFERENCES pull_request(id)
      ON DELETE CASCADE -- this is used for the following thing: delete comment if pr is deleted
);