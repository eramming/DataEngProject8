-- Create a temp staging table that matches the target table
CREATE TEMP TABLE staging_{{TABLE}} AS
SELECT * FROM mls_analysis.{{TABLE}} LIMIT 0;

-- Load CSV data into staging
COPY staging_{{TABLE}}
FROM STDIN
WITH (FORMAT CSV, HEADER TRUE);

-- Insert ONLY into the target table
INSERT INTO mls_analysis.{{TABLE}}
SELECT * FROM staging_{{TABLE}}
ON CONFLICT DO NOTHING;