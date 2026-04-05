CREATE TEMP TABLE staging_census (
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    state_code TEXT NOT NULL,
    population INTEGER,
    median_income REAL,
    education REAL,
    median_age REAL,
    unemployment REAL
);

COPY staging_census (
    city,
    state,
    state_code,
    population,
    median_income,
    education,
    median_age,
    unemployment
)
FROM STDIN
WITH (FORMAT CSV, HEADER TRUE);

INSERT INTO mls_analysis.census (
    city,
    state,
    state_code,
    population,
    median_income,
    education,
    median_age,
    unemployment
)
SELECT
    city,
    state,
    state_code,
    population,
    median_income,
    education,
    median_age,
    unemployment
FROM staging_census
ON CONFLICT (city, state_code) DO NOTHING;