CREATE FUNCTION set_active_model_id() RETURNS TRIGGER AS $$
DECLARE
    active_model_id INTEGER;
BEGIN
    SELECT id INTO active_model_id 
    FROM sentiment_models 
    WHERE is_active = TRUE 
    LIMIT 1;

    IF active_model_id IS NULL THEN
        RAISE EXCEPTION 'No active sentiment analysis model found!';
    END IF;

    NEW.model_id := active_model_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER auto_set_model_id
BEFORE INSERT ON pull_request_comment_sentiment
FOR EACH ROW
EXECUTE FUNCTION set_active_model_id();