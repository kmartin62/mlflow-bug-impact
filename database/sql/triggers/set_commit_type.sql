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