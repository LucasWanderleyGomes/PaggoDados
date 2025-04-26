-- SQLBook: Code
CREATE TABLE signal (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE signal_data (
    id SERIAL PRIMARY KEY,
    signal_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    value FLOAT NOT NULL,
    FOREIGN KEY (signal_id) REFERENCES signal(id)
);