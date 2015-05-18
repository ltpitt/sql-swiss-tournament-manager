-- Table definitions for the tournament project.

-- Remove all data, if present
DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament ENCODING 'utf8';

\c tournament;

CREATE TABLE t_players (

    id SERIAL PRIMARY KEY,
    name TEXT

    );

CREATE TABLE t_tournaments (

    id SERIAL PRIMARY KEY,
    name TEXT

    );

CREATE TABLE t_matches (

    id SERIAL PRIMARY KEY,
    id_tournament INTEGER,
    id_loser INTEGER,
    id_winner INTEGER,

    constraint fk_tournament_id
    foreign key(id_tournament) references t_tournaments(id),

    constraint fk_loser_id
    foreign key(id_loser) references t_players(id),

    constraint fk_winner_id
    foreign key(id_winner) references t_players(id)

    );

CREATE TABLE t_tournaments_players (

    id_player INTEGER,
    id_tournament INTEGER,

    constraint fk_player_id
    foreign key(id_player) references t_players(id),

    constraint fk_tournament_id
    foreign key(id_tournament) references t_tournaments(id),

    primary key (id_player, id_tournament)

  );

CREATE VIEW v_matches_won_per_player AS
    SELECT t_players.id, t_players.name,
    COUNT(t_matches.id_winner) AS total_matches_won
    FROM t_players
    LEFT JOIN t_matches
    ON t_players.id = t_matches.id_winner
    GROUP BY t_players.id
    ORDER BY total_matches_won DESC;

CREATE VIEW v_matches_lost_per_player AS
    SELECT t_players.id, t_players.name,
    COUNT(t_matches.id_loser) AS total_matches_lost
    from t_players LEFT JOIN t_matches
    ON t_players.id = t_matches.id_loser
    GROUP BY t_players.id
    ORDER BY total_matches_lost DESC;

CREATE VIEW v_total_stats AS
    SELECT v_matches_won_per_player.id, v_matches_won_per_player.name,
           v_matches_won_per_player.total_matches_won AS total_matches_won,
           v_matches_lost_per_player.total_matches_lost AS total_matches_lost,
           v_matches_won_per_player.total_matches_won + v_matches_lost_per_player.total_matches_lost as total_matches_played
    FROM v_matches_won_per_player, v_matches_lost_per_player
    WHERE v_matches_won_per_player.id = v_matches_lost_per_player.id;