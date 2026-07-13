SELECT *
FROM supportticket
LIMIT 1;

SELECT COUNT(*) AS total_tickets
FROM supportticket;

SELECT
    status,
    COUNT(*) AS ticket_count
FROM supportticket
GROUP BY status
ORDER BY ticket_count DESC;

SELECT
    priority,
    COUNT(*) AS ticket_count
FROM supportticket
GROUP BY priority
ORDER BY ticket_count DESC;

SELECT
    f.feature_name,
    COUNT(*) AS ticket_count
FROM supportticket s
JOIN feature f
    ON s.feature_id = f.feature_id
GROUP BY f.feature_name
ORDER BY ticket_count DESC;

SELECT
    ticket_category,
    COUNT(*) AS ticket_count
FROM supportticket
GROUP BY ticket_category
ORDER BY ticket_count DESC;

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(*) AS total_tickets
FROM supportticket s
JOIN customer c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_tickets DESC
LIMIT 10;

SELECT
    ROUND(AVG(resolved_at - created_at), 2) AS avg_resolution_days
FROM supportticket
WHERE resolved_at IS NOT NULL;

SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS total_tickets
FROM supportticket
GROUP BY month
ORDER BY month;