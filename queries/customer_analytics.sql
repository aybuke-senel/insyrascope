SELECT *
FROM customer;

SELECT COUNT(*) AS total_customers
FROM customer;

SELECT
    country,
    COUNT(*) AS customer_count
FROM customer
GROUP BY country
ORDER BY customer_count DESC;

SELECT *
FROM customer
LIMIT 1;

SELECT
    subscription_plan,
    COUNT(*) AS customer_count
FROM customer
GROUP BY subscription_plan
ORDER BY customer_count DESC;

SELECT
    customer_status,
    COUNT(*) AS customer_count
FROM customer
GROUP BY customer_status;

SELECT
    DATE_TRUNC('month', signup_date) AS month,
    COUNT(*) AS new_customers
FROM customer
GROUP BY month
ORDER BY month;

SELECT
    customer_id,
    first_name,
    last_name,
    signup_date
FROM customer
ORDER BY signup_date DESC
LIMIT 10;