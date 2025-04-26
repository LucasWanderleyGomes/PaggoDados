CREATE TABLE IF NOT EXISTS data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    wind_speed FLOAT,
    power FLOAT,
    ambient_temperature FLOAT
);

INSERT INTO data (timestamp, wind_speed, power, ambient_temperature)
VALUES 
('2023-01-01 00:00:00', 10.0, 100.0, 20.0),
('2023-01-01 00:01:00', 10.1, 100.1, 20.1),
('2023-01-01 00:02:00', 10.2, 100.2, 20.2);
