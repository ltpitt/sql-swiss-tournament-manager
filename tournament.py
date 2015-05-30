#!/usr/bin/python
# -*- coding: utf-8 -*-
import psycopg2

""" This module contains classes and methods for the Swiss Tournament Manager.
"""

__appname__ = "Swiss Tournament Manager"
__author__ = "Davide Nastri"
__version__ = "1.0"
__license__ = "MIT"


def connect():
    """Connect to the PostgreSQL database.

        Returns:
            a database connection.
    """
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database.
    """

    con = None

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('DELETE FROM t_matches;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e

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
        cur.execute('DELETE FROM t_players;')
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e

    finally:
        if con:
            con.close()


def countPlayers():
    """Counts players in the tournament database

    Returns:
        the number of players currently registered.
    """
    con = None

    try:
        con = connect()
        cur = con.cursor()
        cur.execute('select count(*) as total from t_players;')
        total = cur.fetchone()
        return total[0]

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e

    finally:
        if con:
            con.close()


def registerPlayer(name):
    """Adds a player to the tournament database.

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

    finally:
        if con:
            con.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

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
        rows = cur.execute("select id, name, wins, matches from v_total_stats \
        ORDER BY wins DESC;")
        rows = cur.fetchall()
        return rows

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e

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
        cur.execute("""INSERT INTO t_matches (id_winner, id_loser) VALUES \
        (%s, %s);""", (winner, loser,))
        con.commit()

    except psycopg2.DatabaseError, e:
        print 'Error %s' % e

    finally:
        if con:
            con.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Args:
      tournament: the id number of the tournament played

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings()
    swiss_pairings = []
    for player1, player2 in zip(standings[0::2], standings[1::2]):
        swiss_pairings.append((player1[0], player1[1], player2[0], player2[1]))
    return swiss_pairings
