DROP TABLE IF EXISTS demo;
CREATE TABLE demo (
    row_id      bigserial,
    timestamp   timestamp        NOT NULL,
    client      varchar(64)      NOT NULL,
    handler_id  varchar(128)     NOT NULL,
    temperature double precision NOT NULL,
    humidity    double precision NOT NULL
);
INSERT INTO demo
    (timestamp, client, handler_id, temperature, humidity)
    VALUES ('2017-01-11 20:35:00', 'node04', 'HANDLER00001', 25.0, 80);

