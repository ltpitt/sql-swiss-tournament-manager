-- Table definitions for the tournament project.

-- Remove all data, if present.
\c vagrant
DROP DATABASE tournament;

-- Create tournament database and use it.
CREATE DATABASE tournament ENCODING 'utf8';
\c tournament;

-- Create the table that will hold all players.
CREATE TABLE t_players (

    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL

    );

-- Create the table that will hold all the tournaments.
CREATE TABLE t_tournaments (

    id SERIAL PRIMARY KEY,
    name TEXT

    );

-- Create the table that will hold all match results.
CREATE TABLE t_matches (

    id SERIAL PRIMARY KEY,
    id_tournament INTEGER NOT NULL,
    id_loser INTEGER NOT NULL,
    id_winner INTEGER NOT NULL,

    constraint fk_tournament_id
    foreign key(id_tournament) references t_tournaments(id),

    constraint fk_loser_id
    foreign key(id_loser) references t_players(id),

    constraint fk_winner_id
    foreign key(id_winner) references t_players(id)

    );

-- Create the table that will hold all the player per tournament registrations.
CREATE TABLE t_tournaments_players (

    id_player INTEGER NOT NULL,
    id_tournament INTEGER NOT NULL,

    constraint fk_player_id
    foreign key(id_player) references t_players(id),

    constraint fk_tournament_id
    foreign key(id_tournament) references t_tournaments(id),

    primary key (id_player, id_tournament)

  );


CREATE VIEW v_players_per_tournament AS
    SELECT t_players.id as id_player, t_players.name as player_name, t_tournaments_players.id_tournament
    FROM t_players
    JOIN t_tournaments_players
    ON t_players.id = t_tournaments_players.id_player;

CREATE VIEW v_matches_lost_per_player_per_tournament AS
    SELECT v_players_per_tournament.id_player, v_players_per_tournament.player_name, v_players_per_tournament.id_tournament, COUNT(t_matches.id_loser) AS total_matches_lost
    FROM v_players_per_tournament
    LEFT JOIN t_matches ON v_players_per_tournament.id_player = t_matches.id_loser and v_players_per_tournament.id_tournament = t_matches.id_tournament
    GROUP BY v_players_per_tournament.id_player, v_players_per_tournament.player_name, v_players_per_tournament.id_tournament
    ORDER BY total_matches_lost DESC;

CREATE VIEW v_matches_won_per_player_per_tournament AS
    SELECT v_players_per_tournament.id_player, v_players_per_tournament.player_name, v_players_per_tournament.id_tournament, COUNT(t_matches.id_winner) AS total_matches_won
    FROM v_players_per_tournament
    LEFT JOIN t_matches ON v_players_per_tournament.id_player = t_matches.id_winner AND v_players_per_tournament.id_tournament = t_matches.id_tournament
    GROUP BY v_players_per_tournament.id_player, v_players_per_tournament.player_name, v_players_per_tournament.id_tournament
    ORDER BY total_matches_won DESC;

CREATE VIEW v_total_stats AS
    SELECT v_matches_won_per_player_per_tournament.id_player as id, v_matches_won_per_player_per_tournament.player_name as name,
           v_matches_won_per_player_per_tournament.total_matches_won as wins,
           v_matches_lost_per_player_per_tournament.total_matches_lost as losses,
           v_matches_won_per_player_per_tournament.id_tournament
    FROM v_matches_won_per_player_per_tournament, v_matches_lost_per_player_per_tournament
    WHERE v_matches_won_per_player_per_tournament.id_player = v_matches_lost_per_player_per_tournament.id_player AND v_matches_won_per_player_per_tournament.id_tournament = v_matches_lost_per_player_per_tournament.id_tournament
    GROUP BY v_matches_won_per_player_per_tournament.id_player, v_matches_won_per_player_per_tournament.player_name,
           v_matches_won_per_player_per_tournament.total_matches_won,
           v_matches_lost_per_player_per_tournament.total_matches_lost,
           v_matches_won_per_player_per_tournament.id_tournament;

