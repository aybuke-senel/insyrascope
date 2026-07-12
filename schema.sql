CREATE TABLE Customer (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    country VARCHAR(50),
    subscription_plan VARCHAR(20),
    customer_status VARCHAR(20),
    signup_date DATE
);

CREATE TABLE Feature (
    feature_id VARCHAR(20) PRIMARY KEY,
    feature_name VARCHAR(100),
    module VARCHAR(100),
    is_active BOOLEAN
);

CREATE TABLE ProductUsage (
    usage_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    feature_id VARCHAR(20) NOT NULL,
    usage_count INT,
    session_duration INT,
    last_device VARCHAR(50),
    last_used DATE,

    CONSTRAINT fk_usage_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id),

    CONSTRAINT fk_usage_feature
        FOREIGN KEY (feature_id)
        REFERENCES Feature(feature_id)
);

CREATE TABLE CustomerFeedback (
    feedback_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    feature_id VARCHAR(20),
    rating INT,
    feedback_category VARCHAR(50),
    comment TEXT,
    sentiment VARCHAR(20),
    created_at DATE,

    CONSTRAINT fk_feedback_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id),

    CONSTRAINT fk_feedback_feature
        FOREIGN KEY (feature_id)
        REFERENCES Feature(feature_id)
);

CREATE TABLE SupportTicket (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    feature_id VARCHAR(20),
    ticket_category VARCHAR(50),
    priority VARCHAR(20),
    status VARCHAR(20),
    assigned_team VARCHAR(50),
    description TEXT,
    created_at DATE,
    resolved_at DATE,

    CONSTRAINT fk_ticket_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id),

    CONSTRAINT fk_ticket_feature
        FOREIGN KEY (feature_id)
        REFERENCES Feature(feature_id)
);

CREATE TABLE SecurityEvent (
    event_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    event_type VARCHAR(50),
    severity VARCHAR(20),
    status VARCHAR(20),
    description TEXT,
    event_time TIMESTAMP,

    CONSTRAINT fk_security_customer
        FOREIGN KEY (customer_id)
        REFERENCES Customer(customer_id)
);