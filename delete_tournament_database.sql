-- This script completely drops all the tables in the tournament database project.
\c tournament;
DROP TABLE t_matches CASCADE;
DROP TABLE t_tournaments_players CASCADE;
DROP TABLE t_tournaments CASCADE;
DROP TABLE t_players CASCADE;
\c vagrant;
DROP DATABASE tournament;
