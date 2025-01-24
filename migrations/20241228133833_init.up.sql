CREATE EXTENSION vector;

CREATE TABLE places (
    place_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    embedding vector(3072),
    metadata jsonb
);


CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL NOT NULL PRIMARY KEY,
    telegram_id BIGINT NOT NULL UNIQUE,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    language_code TEXT,
    came_from TEXT,
    created_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
