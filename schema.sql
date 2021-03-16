CREATE TABLE IF NOT EXISTS nisdev (
    user_id BIGINT PRIMARY KEY,
    name VARCHAR(25),
    who VARCHAR(7),
    accepted BOOLEAN DEFAULT false
)