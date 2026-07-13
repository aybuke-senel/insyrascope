SELECT *
FROM securityevent
LIMIT 1;

SELECT COUNT(*) AS total_events
FROM securityevent;

SELECT
    severity,
    COUNT(*) AS event_count
FROM securityevent
GROUP BY severity
ORDER BY event_count DESC;

SELECT
    event_type,
    COUNT(*) AS event_count
FROM securityevent
GROUP BY event_type
ORDER BY event_count DESC;

SELECT
    status,
    COUNT(*) AS event_count
FROM securityevent
GROUP BY status
ORDER BY event_count DESC;

SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(*) AS total_events
FROM securityevent s
JOIN customer c
    ON s.customer_id = c.customer_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name
ORDER BY total_events DESC
LIMIT 10;

SELECT
    DATE_TRUNC('month', event_time) AS month,
    COUNT(*) AS total_events
FROM securityevent
GROUP BY month
ORDER BY month;