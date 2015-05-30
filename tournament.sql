-- Table definitions for the Swiss Tournament Manager.

-- Removes tournament database.
\c vagrant
DROP DATABASE IF EXISTS tournament;

-- Creates tournament database and use it.
CREATE DATABASE tournament ENCODING 'utf8';
\c tournament;

-- Creates the table that will hold all players.
CREATE TABLE t_players (

    id SERIAL PRIMARY KEY,
    name TEXT

    );

-- Creates the table that will hold all match results.
CREATE TABLE t_matches (

    id SERIAL PRIMARY KEY,
    id_loser INTEGER,
    id_winner INTEGER,

    constraint fk_loser_id
    foreign key(id_loser) references t_players(id),

    constraint fk_winner_id
    foreign key(id_winner) references t_players(id)

    );

-- Creates the view that will count all matches won per player.
CREATE VIEW v_matches_won_per_player AS
    SELECT t_players.id, t_players.name,
    COUNT(t_matches.id_winner) AS total_matches_won
    FROM t_players
    LEFT JOIN t_matches
    ON t_players.id = t_matches.id_winner
    GROUP BY t_players.id
    ORDER BY total_matches_won DESC;

-- Creates the view that will count all matches lost per player.
CREATE VIEW v_matches_lost_per_player AS
    SELECT t_players.id, t_players.name,
    COUNT(t_matches.id_loser) AS total_matches_lost
    from t_players LEFT JOIN t_matches
    ON t_players.id = t_matches.id_loser
    GROUP BY t_players.id
    ORDER BY total_matches_lost DESC;

-- Creates the view with total stats per player.
CREATE VIEW v_total_stats AS
    SELECT v_matches_won_per_player.id, v_matches_won_per_player.name,
           v_matches_won_per_player.total_matches_won AS wins,
           v_matches_lost_per_player.total_matches_lost AS losses,
           v_matches_won_per_player.total_matches_won + v_matches_lost_per_player.total_matches_lost as matches
    FROM v_matches_won_per_player, v_matches_lost_per_player
    WHERE v_matches_won_per_player.id = v_matches_lost_per_player.id;