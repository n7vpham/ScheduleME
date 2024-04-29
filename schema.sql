CREATE TABLE IF NOT EXISTS users (
    user_id             SERIAL,
    user_fname          VARCHAR(255)    NOT NULL,
    user_lname          VARCHAR(255)    NOT NULL,
    user_email          VARCHAR(255)    UNIQUE NOT NULL,
    user_password       VARCHAR(255)    NOT NULL,
    user_since          TIMESTAMP       DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id)
);

CREATE TABLE IF NOT EXISTS events (
    event_id            SERIAL,
    host_id             INT             NOT NULL, 
    event_name          VARCHAR(255)    NOT NULL,
    event_description   VARCHAR(255)    NOT NULL,
    start_time          TIMESTAMP       NOT NULL,
    end_time            TIMESTAMP       NOT NULL,
    event_address       VARCHAR(255)    NOT NULL,       
    PRIMARY KEY (event_id), 
    FOREIGN KEY (host_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

-- Run this only if you have the old tables
alter table events rename  column title to event_name;
alter table events rename  column description to event_description;
alter table events rename  column address to event_address;


-- Add more if you want(For testing purposes)
Insert into users (user_fname, user_lname, user_email, user_password) values ('John', 'Doe', 'johndoe@gmail.com', 'password'); 
Insert into users (user_fname, user_lname, user_email, user_password) values ('Jane', 'Doe', 'janedoe@gmail.com', 'password1'); 

Insert into events (host_id, event_name, event_description, start_time, end_time, event_address) values (1, 'TOWNHALL MEETING', 'Come celebrate my birthday', '2021-12-12 12:00:00.436454', '2021-12-12 15:00:00.436454', '1234 Elm St');    
Insert into events (host_id, event_name, event_description, start_time, end_time, event_address) values (2, 'CAREER FAIR', 'UNCC CS Major career fair fo the semester', '2021-12-12 12:00:00.464515', '2021-12-12 15:00:00.464515', '1234 Elm St');


-- EXPERIMENTAL
CREATE TABLE IF NOT EXISTS comment (
    comment_id          SERIAL,
    content             VARCHAR(255)   NOT NULL,
    event_id            INT            NOT NULL,
    user_id             INT            NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TYPE vote as  ENUM('thumbsup', 'thumbsdown');

CREATE TABLE IF NOT EXISTS reaction (
    reaction_id          SERIAL,
    reaction_type        vote,
    event_id             INT            NOT NULL,
    user_id              INT            NOT NULL,
    PRIMARY KEY (reaction_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
);

SELECT e.name, e.start_time, e.end_time, e.description, u.user_username AS organizer, c.content AS comment, r.reaction_type
FROM events e
INNER JOIN users u ON e.host_id = u.user_id
LEFT JOIN comment c ON e.event_id = c.event_id
LEFT JOIN reaction r ON e.event_id = r.event_id
WHERE e.name = 'TOWNHALL MEETING';

