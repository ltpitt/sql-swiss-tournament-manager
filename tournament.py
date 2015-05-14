#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import sys


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('TRUNCATE t_matches CASCADE;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()



def deletePlayers():
    """Remove all the player records from the database."""
    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('TRUNCATE t_players CASCADE;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()



def countPlayers():
    """Returns the number of players currently registered."""
    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('select count(*) as total from t_players;')
        total = cur.fetchone()
        return total[0]

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()



def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute("INSERT INTO t_players (name) VALUES (%s);", (name,))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    con = None

    try:

        con = connect()
        cur = con.cursor()
        rows = cur.execute("select t_players.id, t_players.name, CASE WHEN v_total_stats.total_wins IS NULL THEN 0 ELSE v_total_stats.total_wins END, CASE WHEN v_total_stats.total_matches_played IS NULL THEN 0 ELSE v_total_stats.total_matches_played END from t_players left join v_total_stats on t_players.id = v_total_stats.id ORDER BY total_matches_played, total_wins DESC;")
        rows = cur.fetchall()
        return rows
        con.commit()


    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    con = None

    try:

        con = connect()
        cur = con.cursor()
        #cur.execute("INSERT INTO t_matches (id_player_a, id_player_b, id_winner) VALUES (%s)"), (winner, loser, winner,)
        cur.execute('INSERT INTO t_matches (id_player_a, id_player_b, id_winner) VALUES ('+str(winner)+','+str(loser)+','+str(winner)+')')
        con.commit()


    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    swiss_pairings = []
    tmp_list = []
    counter = 0
    for player in standings:
        counter += 1
        if counter % 2 == 0:
            tmp_list.append(player[0])
            tmp_list.append(player[1])
            swiss_pairings.append(tuple(tmp_list))
            tmp_list = []
        else:
            tmp_list.append(player[0])
            tmp_list.append(player[1])
    return swiss_pairings



