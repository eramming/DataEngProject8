CREATE TABLE IF NOT EXISTS mls_analysis.seasons (
    season_id INT PRIMARY KEY,
    year INT,
    season_type TEXT
);

CREATE TABLE IF NOT EXISTS mls_analysis.teams (
    team_id INT PRIMARY KEY,
    team_name TEXT,
    stadium TEXT
);

CREATE TABLE IF NOT EXISTS mls_analysis.games (
    game_id INT PRIMARY KEY,
    stadium TEXT,
    season_id INT,
    game_date DATE,
    attendance INT
);

CREATE TABLE IF NOT EXISTS mls_analysis.game_teams (
    game_id INT,
    team_id INT,
    home_away TEXT,
    score INT,
    winner_flag BOOLEAN,
    PRIMARY KEY (game_id, team_id)
);
