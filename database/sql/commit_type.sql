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


-- trigger
CREATE OR REPLACE FUNCTION set_commit_type() 
RETURNS TRIGGER AS $$
BEGIN
    NEW.commit_type_id := (
        SELECT id 
        FROM commit_type 
        WHERE name = LOWER(SPLIT_PART(NEW.message, ':', 1))
        LIMIT 1
    );

    IF NEW.commit_type_id IS NULL THEN
        NEW.commit_type_id := (SELECT id FROM commit_type WHERE name = 'other');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER commit_type_trigger
BEFORE INSERT ON git_commit
FOR EACH ROW
EXECUTE FUNCTION set_commit_type();