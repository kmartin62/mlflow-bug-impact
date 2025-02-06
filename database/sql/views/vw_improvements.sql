CREATE VIEW vw_improvements AS
SELECT pr.title, mi.percentage_change_accuracy, mi.percentage_change_recall, percentage_change_precision, percentage_change_f1, percentage_change_log_loss FROM model_improvements mi
INNER JOIN git_commit gc ON gc.hash = mi.commit_hash
INNER JOIN pull_request pr ON pr.id = gc.pr_id