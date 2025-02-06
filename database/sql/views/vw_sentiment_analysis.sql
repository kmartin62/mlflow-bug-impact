CREATE VIEW vw_sentiment_analysis AS
SELECT pr.id, pr.title, pr.author, pr.comments_count, prcs.sentiment_label FROM pull_request_comment_sentiment prcs
INNER JOIN pull_request pr ON pr.id = prcs.pr_id