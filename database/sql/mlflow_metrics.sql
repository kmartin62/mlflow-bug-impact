CREATE TABLE IF NOT EXISTS mlflow_metrics (
    id SERIAL PRIMARY KEY,
    experiment_id TEXT NOT NULL, 
    run_id TEXT NOT NULL UNIQUE, 
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    model TEXT NOT NULL, 
    accuracy FLOAT, 
    recall FLOAT, 
    precision FLOAT, 
    f1_score FLOAT, 
    roc_auc FLOAT, 
    log_loss FLOAT, 
    commit_hash TEXT NOT NULL REFERENCES git_commit(hash) ON DELETE CASCADE,
    mongo_id TEXT NOT NULL
);