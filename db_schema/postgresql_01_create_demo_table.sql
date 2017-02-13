DROP TABLE IF EXISTS demo;
CREATE TABLE demo (
    row_id      bigserial,
    timestamp   timestamp        NOT NULL,
    client      varchar(64)      NOT NULL,
    handler_id  varchar(128)     NOT NULL,
    temperature double precision NOT NULL,
    humidity    double precision NOT NULL
);
