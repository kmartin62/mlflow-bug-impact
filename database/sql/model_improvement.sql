CREATE TABLE IF NOT EXISTS model_improvements (
    id SERIAL PRIMARY KEY,
    pr_id INTEGER NOT NULL REFERENCES pull_request(id) ON DELETE CASCADE,
    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE REFERENCES mlflow_metrics(run_id) ON DELETE CASCADE,
    metric TEXT NOT NULL,
    previous_value FLOAT,
    new_value FLOAT NOT NULL,
    percentage_change FLOAT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);