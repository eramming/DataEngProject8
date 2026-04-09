CREATE TABLE IF NOT EXISTS mls_analysis.venues (
    id SERIAL PRIMARY KEY,
    team TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    lat REAL,
    lon REAL,
    stadium TEXT NOT NULL,
    capacity INTEGER
);

