USE makina;
CREATE TABLE uptime (
    row_id      bigint       AUTO_INCREMENT,
    timestamp   timestamp    NOT NULL,
    client      varchar(64)  NOT NULL,
    message     varchar(128) NOT NULL,
    PRIMARY KEY (row_id)
);
INSERT INTO uptime
    (timestamp, client, message)
    VALUES ('2017-01-11 20:35:00', 'node04', 'hello world!');

