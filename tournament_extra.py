#!/usr/bin/python
# -*- coding: utf-8 -*-
""" This module contains classes and methods for the Swiss Tournament Manager.
"""

__appname__ = "Swiss Tournament Manager"
__author__ = "Davide Nastri"
__version__ = "0.1beta"
__license__ = "MIT"

import psycopg2
import sys


def connect():
    """Connects to the PostgreSQL database.

    Returns:
        A database connection.
    """

    return psycopg2.connect("dbname=tournament")


def deleteTournaments():
    """Removes all the tournaments records from the database.
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('TRUNCATE t_tournaments CASCADE;')
        cur.execute('ALTER SEQUENCE t_tournaments_id_seq RESTART WITH 1;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def deleteMatches():
    """Removes all the match records from the database.
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('TRUNCATE t_matches CASCADE;')
        cur.execute('ALTER SEQUENCE t_matches_id_seq RESTART WITH 1;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def deletePlayers():
    """Remove all the player records from the database.
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('TRUNCATE t_players CASCADE;')
        cur.execute('ALTER SEQUENCE t_players_id_seq RESTART WITH 1;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def countPlayers(tournament):
    """Returns the number of players currently registered.

    Args:
      tournament: the id number of the tournament played.
      If number 0 is used it selects all tournaments

    Returns:
      Total number of players in selected tournament or all tournaments
    """

    if tournament == 0:

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

        con = None

    else:

        try:

            con = connect()
            cur = con.cursor()
            cur.execute("""select count(*) as total from t_tournaments_players where id_tournament = %s;""",
                        (tournament, ))
            total = cur.fetchone()
            return total[0]

        except psycopg2.DatabaseError, e:
            print 'Error %s' % e
            sys.exit(1)


        finally:

            if con:
                con.close()


def countMatches():
    """Returns the number of matches currently registered.
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('select count(*) as total from t_matches;')
        total = cur.fetchone()
        return total[0]

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def countTournaments():
    """Returns the number of tournaments currently registered.
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute('select count(*) as total from t_tournaments;')
        total = cur.fetchone()
        return total[0]

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def registerPlayer(name, surname, email):
    """Adds a player to the tournament database.
  
    Args:
      name: the player's full name (need not be unique).
      surname: the player's full surname (need not be unique).
      email: the player's full surname (need to be unique).
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute("""INSERT INTO t_players (name, surname, email) VALUES (%s, %s, %s);""", (name, surname, email, ))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def registerPlayerToTournament(player, tournament):
    """Adds an existing player to an existing tournament.

    Args:
      player:     the player's id
      tournament: the tournament's id
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute("""INSERT INTO t_tournaments_players (id_player, id_tournament) VALUES (%s, %s);""",
                    (player, tournament, ))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def registerTournament(name):
    """Adds a tournament to the tournament database.
  
    Args:
      name: the tournament's full name (need not be unique)
    """

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute("INSERT INTO t_tournaments (name) VALUES (%s);", (name, ))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def playerStandings(tournament):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      tournament: the id number of the tournament played.

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
        standings = cur.execute(
            """SELECT id, name, wins, wins + losses as matches from v_total_stats WHERE id_tournament = %s GROUP BY id, name, wins, matches ORDER BY wins;""",
            (tournament,))
        standings = cur.fetchall()
        return standings

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)

    finally:

        if con:
            con.close()


def reportMatch(tournament, loser, winner):
    """Records the outcome of a single match between two players.

    Args:
      tournament: the id number of the tournament played
      loser:  the id number of the player who lost
      winner:  the id number of the player who won

    Returns:
      If a rematch is registered it returns this string:
      "ERROR: You tried to register a rematch"
      If player/s are not registered in tournament it returns this string:
      "ERROR: One/Both of the players is not registered in the specified tournament"
      If a player is playing with himself it returns this string:
      "ERROR: A player cannot play alone"
    """

    if loser == winner:
        return "ERROR: A player cannot play alone"

    con = None

    try:

        con = connect()
        cur = con.cursor()
        cur.execute(
            """SELECT COUNT(*) FROM t_tournaments_players WHERE id_tournament = %s AND (id_player = %s OR id_player = %s);""",
            (tournament, loser, winner,))
        number_of_players_in_tournament = cur.fetchone()
        if number_of_players_in_tournament[0] < 2:
            return "ERROR: One of the players is not registered in the specified tournament"
        elif number_of_players_in_tournament[0] == 2:
            cur.execute(
                """SELECT COUNT(*) FROM t_matches WHERE id_tournament = %s AND (id_winner = %s OR id_winner = %s) AND (id_loser = %s OR id_loser = %s);""",
                (tournament, winner, loser, winner, loser,))
            rematch = cur.fetchone()
            if rematch[0] > 0:
                not_a_rematch = False
            else:
                not_a_rematch = True
            if not_a_rematch:
                cur.execute("""INSERT INTO t_matches (id_tournament, id_loser, id_winner) VALUES (%s, %s, %s);""",
                            (tournament, loser, winner,))
                con.commit()
            else:
                return "ERROR: You tried to register a rematch"

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


    finally:

        if con:
            con.close()


def swissPairings(tournament):
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament: the id number of the tournament played

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings(tournament)
    swiss_pairings = []
    for player1, player2 in zip(standings[0::2], standings[1::2]):
        swiss_pairings.append((player1[0], player1[1], player2[0], player2[1]))
    return swiss_pairings
