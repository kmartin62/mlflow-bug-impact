CREATE TABLE IF NOT EXISTS champion_model (
    id SERIAL PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE REFERENCES mlflow_metrics(run_id) ON DELETE CASCADE,
    metric TEXT NOT NULL,
    metric_value FLOAT NOT NULL,
    selected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);