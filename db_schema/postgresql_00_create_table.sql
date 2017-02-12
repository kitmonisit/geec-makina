CREATE TABLE uptime (
    row_id      bigserial    PRIMARY KEY,
    timestamp   timestamp    NOT NULL,
    client      varchar(64)  NOT NULL,
    message     varchar(128) NOT NULL
);
INSERT INTO uptime
    (timestamp, client, message)
    VALUES ('2017-01-11 20:35:00', 'node04', 'hello world!');

