COPY mls_analysis.venues (team, city, state, lat, lon, stadium)
FROM STDIN
WITH (FORMAT CSV, HEADER TRUE)