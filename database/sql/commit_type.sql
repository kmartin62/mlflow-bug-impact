CREATE TABLE IF NOT EXISTS commit_type (
	id SERIAL PRIMARY KEY,
	name VARCHAR(20) UNIQUE NOT NULL,
	description TEXT
);

INSERT INTO commit_type (name, description) VALUES 
    ('fix', 'Bug fix'),
    ('feat', 'New feature'),
    ('chore', 'Maintenance task'),
    ('refactor', 'Code refactor'),
    ('docs', 'Documentation changes'),
    ('style', 'Code style changes'),
    ('test', 'Test related changes'),
    ('perf', 'Performance improvements'),
    ('other', 'Uncategorized changes');