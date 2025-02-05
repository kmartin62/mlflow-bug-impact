CREATE TABLE IF NOT EXISTS champion_model (
    id SERIAL PRIMARY KEY,
    experiment_id TEXT NOT NULL,
    run_id TEXT NOT NULL UNIQUE REFERENCES mlflow_metrics(run_id) ON DELETE CASCADE,
    metric TEXT NOT NULL,
    metric_value FLOAT NOT NULL,
    selected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE OR REPLACE FUNCTION update_champion_model()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM champion_model WHERE is_active = TRUE) THEN
        INSERT INTO champion_model (experiment_id, run_id, metric, metric_value, selected_at, is_active)
        VALUES (NEW.experiment_id, NEW.run_id, 'accuracy', NEW.accuracy, NOW(), TRUE);
    
    ELSIF NEW.accuracy > (SELECT metric_value FROM champion_model WHERE is_active = TRUE) THEN
        UPDATE champion_model
        SET is_active = FALSE
        WHERE is_active = TRUE;

        INSERT INTO champion_model (experiment_id, run_id, metric, metric_value, selected_at, is_active)
        VALUES (NEW.experiment_id, NEW.run_id, 'accuracy', NEW.accuracy, NOW(), TRUE);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_and_update_champion
AFTER INSERT ON mlflow_metrics
FOR EACH ROW
EXECUTE FUNCTION update_champion_model();
