INSERT INTO t_players (name) VALUES ('Primo');
INSERT INTO t_players (name) VALUES ('Secondo');
INSERT INTO t_players (name) VALUES ('Terzo');
INSERT INTO t_players (name) VALUES ('Quarto');
INSERT INTO t_players (name) VALUES ('Quinto');

INSERT INTO t_tournaments (name) VALUES ('Scacchi');

INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 2, 1);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 3, 1);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 4, 1);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 2, 2);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 2, 2);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 1, 3);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 5, 3);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 5, 5);
INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (1, 2, 1);