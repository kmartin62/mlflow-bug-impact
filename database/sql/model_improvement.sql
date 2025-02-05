CREATE TABLE IF NOT EXISTS model_improvements (
    id SERIAL PRIMARY KEY,
    commit_hash TEXT NOT NULL REFERENCES git_commit(hash) ON DELETE CASCADE,
    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE REFERENCES mlflow_metrics(run_id) ON DELETE CASCADE,
    percentage_change_accuracy FLOAT,
    percentage_change_recall FLOAT,
    percentage_change_precision FLOAT,
    percentage_change_f1 FLOAT,
    percentage_change_log_loss FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);