CREATE TABLE IF NOT EXISTS mls_analysis.census (
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    state_code TEXT NOT NULL,
    population INTEGER,
    median_income REAL,
    education REAL,
    median_age REAL,
    unemployment REAL,
    PRIMARY KEY (city, state_code)
);