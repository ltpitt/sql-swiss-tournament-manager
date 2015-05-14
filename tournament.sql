-- Table definitions for the tournament project.
--
-- Put your SQL 'CREATE TABLE' statements in this file; also 'CREATE VIEW'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE t_matches CASCADE;
DROP TABLE t_tournaments_players CASCADE;
DROP TABLE t_tournaments CASCADE;
DROP TABLE t_players CASCADE;
DROP VIEW v_total_matches_a CASCADE;
DROP VIEW v_total_matches_b CASCADE;
DROP VIEW v_total_winners CASCADE;


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
    id_player_a INTEGER,
    id_player_b INTEGER,
    id_winner INTEGER,

    constraint fk_tournament_id
    foreign key(id_tournament) references t_tournaments(id),

    constraint fk_player_a_id
    foreign key(id_player_a) references t_players(id),

    constraint fk_player_b_id
    foreign key(id_player_b) references t_players(id),

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

INSERT INTO t_players (name) VALUES ('Primo');
INSERT INTO t_players (name) VALUES ('Secondo');
INSERT INTO t_players (name) VALUES ('Terzo');
INSERT INTO t_players (name) VALUES ('Quarto');
INSERT INTO t_players (name) VALUES ('Quinto');

INSERT INTO t_tournaments (name) VALUES ('Scacchi');

INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 1, 2, 1);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 1, 3, 1);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 1, 4, 1);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 2, 2, 2);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 5, 2, 2);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 3, 1, 3);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 3, 5, 3);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 2, 5, 5);
INSERT INTO t_matches (id_tournament, id_player_a, id_player_b, id_winner) VALUES (1, 1, 2, 1);

CREATE VIEW v_total_winners AS
SELECT t_players.id, t_players.name, COUNT(id_winner) as total_wins from t_players LEFT JOIN t_matches ON t_players.id = t_matches.id_winner GROUP BY t_players.id, t_players.name ORDER BY total_wins DESC;

CREATE VIEW v_total_matches_a AS
SELECT t_players.id, t_players.name, COUNT(t_matches.id_player_a) as total_matches from t_players LEFT JOIN t_matches ON t_players.id = t_matches.id_player_a GROUP BY t_players.id ORDER BY total_matches DESC;


CREATE VIEW v_total_matches_b AS
SELECT t_players.id, t_players.name, COUNT(t_matches.id_player_b) as total_matches from t_players LEFT JOIN t_matches ON t_players.id = t_matches.id_player_b GROUP BY t_players.id ORDER BY total_matches DESC;


CREATE VIEW v_total_matches AS
SELECT v_total_matches_a.id, v_total_matches_a.name, v_total_matches_a.total_matches as total_matches_a, v_total_matches_b.total_matches as total_matches_b, v_total_matches_a.total_matches + v_total_matches_b.total_matches as total_matches_played FROM v_total_matches_a, v_total_matches_b WHERE v_total_matches_a.id = v_total_matches_b.id;

CREATE VIEW v_total_stats AS
SELECT v_total_matches.id, v_total_matches.name, v_total_winners.total_wins, v_total_matches.total_matches_played from v_total_matches, v_total_winners where v_total_matches.id = v_total_winners.id;

