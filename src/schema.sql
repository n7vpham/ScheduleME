CREATE TABLE IF NOT EXISTS users (
    user_id             SERIAL,
    user_fname          VARCHAR(255)    NOT NULL,
    user_lname          VARCHAR(255)    NOT NULL,
    user_username       VARCHAR(255)    UNIQUE NOT NULL,
    user_password       VARCHAR(255)    NOT NULL,
    user_since          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id            SERIAL,
    event_description   VARCHAR(255)    NOT NULL, 
    event_when          VARCHAR(255)    NOT NULL,
    event_where         VARCHAR(255)    NOT NULL,
    host_id             INT             NOT NULL,
    event_timestamp     TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    analytic_type       VARCHAR(255)    DEFAULT 'create event',            
    PRIMARY KEY (event_id), 
    FOREIGN KEY (host_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);