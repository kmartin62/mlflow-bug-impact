CREATE TABLE IF NOT EXISTS sentiment_models (
	id SERIAL PRIMARY KEY,
	sentiment_analysis_model TEXT NOT NULL,
	added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	is_active BOOLEAN NOT NULL DEFAULT FALSE
);

INSERT INTO sentiment_models (sentiment_analysis_model, is_active) 
VALUES ('cardiffnlp/twitter-roberta-base-sentiment-latest', true);

CREATE UNIQUE INDEX unique_active_model ON sentiment_models (is_active)
WHERE is_active = TRUE; -- this makes sure that we have ONLY ONE active model, therefore no two models can be is_active = true