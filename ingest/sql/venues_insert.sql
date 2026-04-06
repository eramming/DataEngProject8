CREATE TEMP TABLE staging_venues (
    id SERIAL PRIMARY KEY,
    team TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    lat REAL,
    lon REAL,
    stadium TEXT NOT NULL
    capacity INTEGER
);

COPY staging_venues (team, city, state, lat, lon, stadium)
FROM STDIN
WITH (FORMAT CSV, HEADER TRUE);



INSERT INTO mls_analysis.venues (team, city, state, lat, lon, stadium)
SELECT team, city, state, lat, lon, stadium
FROM staging_venues
ON CONFLICT (team) DO NOTHING;