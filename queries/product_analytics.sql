SELECT *
FROM productusage
LIMIT 1;

SELECT *
FROM feature
LIMIT 1;

SELECT
    f.feature_name,
    SUM(p.usage_count) AS total_usage
FROM productusage p
JOIN feature f
    ON p.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY total_usage DESC;

SELECT
    f.feature_name,
    ROUND(AVG(p.session_duration),2) AS avg_session_duration
FROM productusage p
JOIN feature f
    ON p.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY avg_session_duration DESC;

SELECT
    f.module,
    SUM(p.usage_count) AS total_usage
FROM productusage p
JOIN feature f
    ON p.feature_id = f.feature_id
GROUP BY f.module
ORDER BY total_usage DESC;

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    SUM(p.usage_count) AS total_usage
FROM productusage p
JOIN customer c
    ON p.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_usage DESC
LIMIT 10;

SELECT
    f.feature_name,
    COUNT(DISTINCT p.customer_id) AS unique_users
FROM productusage p
JOIN feature f
    ON p.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY unique_users DESC;

=====================================

SELECT *
FROM customerfeedback
LIMIT 1;

SELECT
    f.feature_name,
    ROUND(AVG(cf.rating),2) AS average_rating
FROM customerfeedback cf
JOIN feature f
    ON cf.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY average_rating DESC;

SELECT
    f.feature_name,
    ROUND(AVG(cf.rating),2) AS average_rating
FROM customerfeedback cf
JOIN feature f
    ON cf.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY average_rating ASC;

SELECT
    f.feature_name,
    COUNT(*) AS feedback_count
FROM customerfeedback cf
JOIN feature f
    ON cf.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY feedback_count DESC;

SELECT
    sentiment,
    COUNT(*) AS total_feedback
FROM customerfeedback
GROUP BY sentiment
ORDER BY total_feedback DESC;

SELECT
    feedback_category,
    COUNT(*) AS total_feedback
FROM customerfeedback
GROUP BY feedback_category
ORDER BY total_feedback DESC;