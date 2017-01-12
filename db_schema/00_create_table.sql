DROP TABLE uptime;
CREATE TABLE uptime (
    row_id      bigserial    PRIMARY KEY,
    timestamp   timestamp    NOT NULL,
    client_name varchar(64)  NOT NULL,
    message     varchar(128) NOT NULL
);
INSERT INTO uptime
    (timestamp, client_name, message)
    VALUES ('2017-01-11 20:35:00', 'node_04', 'hello world!');
