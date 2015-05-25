#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *
import os


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


def testDeleteTournaments():
    deleteMatches()
    print "1. Tournaments can be deleted."


def testDeleteMatches():
    deleteMatches()
    print "2. Matches can be deleted."


def testDeletePlayers():
    deletePlayers()
    print "3. Players can be deleted."


def testCountTournaments():
    deleteTournaments()
    c = countTournaments()
    if c == '0':
        raise TypeError(
            "countTournaments() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countTournaments should return zero.")
    print "4. After deleting, countTournaments() returns zero."


def testCountMatches():
    deleteMatches()
    c = countMatches()
    if c == '0':
        raise TypeError(
            "countMatches() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countMatches should return zero.")
    print "5. After deleting, countMatches() returns zero."


def testCountPlayers():
    deletePlayers()
    c = countPlayers(0)
    if c == '0':
        raise TypeError(
            "countPlayers() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "6. After deleting, countPlayers() returns zero."


def testRegisterTournament():
    registerTournament("Tennis")
    c = countTournaments()
    if c != 1:
        raise ValueError(
            "After one tournament is registered, countTournaments() should be 1.")
    print "7. After registering a tournament, countTournaments() returns 1."


def testRegisterPlayer():
    registerPlayer("Player", "One", "playerone@tournament.com")
    c = countPlayers(0)
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "8. After registering a player, countPlayers() returns 1."


def testRegisterPlayerToTournament():
    registerPlayerToTournament(1, 1)

    c = countPlayers(1)
    if c != 1:
        raise ValueError(
            "After one player registers to tournament 1, countPlayers(1) should be 1.")
    print "9. After registering a player to tournament 1, countPlayers(1) returns 1."


def testRegisterCountDelete():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerPlayer("Player1", "One", "playerone@tournament.com")
    registerPlayer("Player2", "Two", "playertwo@tournament.com")
    registerPlayer("Player3", "Three", "playerthree@tournament.com")
    registerPlayer("Player4", "Four", "playerfour@tournament.com")
    c = countPlayers(0)
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers(0)
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "10. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerPlayer("Player1", "One", "playerone@tournament.com")
    registerPlayer("Player2", "Two", "playertwo@tournament.com")
    registerTournament("Tennis")
    registerPlayerToTournament(1, 1)
    registerPlayerToTournament(2, 1)
    standings = playerStandings(1)
    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Player1", "Player2"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "11. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerPlayer("Player1", "One", "playerone@tournament.com")
    registerPlayer("Player2", "Two", "playertwo@tournament.com")
    registerPlayer("Player3", "Three", "playerthree@tournament.com")
    registerPlayer("Player4", "Four", "playerfour@tournament.com")
    registerTournament("Tennis")
    registerPlayerToTournament(1, 1)
    registerPlayerToTournament(2, 1)
    registerPlayerToTournament(3, 1)
    registerPlayerToTournament(4, 1)
    standings = playerStandings(1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(1, id1, id2)
    reportMatch(1, id3, id4)

    if reportMatch(1, id4, 200) != "ERROR: One of the players is not registered in the specified tournament":
        raise ValueError("It is possible to register a match for a player not registered in the specified tournament.")

    if reportMatch(1, 1, 2) != "ERROR: You tried to register a rematch":
        raise ValueError("It is possible to play a rematch.")

    if reportMatch(1, 2, 1) != "ERROR: You tried to register a rematch":
        raise ValueError("It is possible to play a rematch.")

    if reportMatch(1, 1, 1) != "ERROR: A player cannot play alone":
        raise ValueError("It is possible to have a match with the same player both winning and losing.")

    standings = playerStandings(1)

    for (id_player, name, wins, matches) in standings:
        if matches != 1:
            raise ValueError("Each player should have one match recorded.")
        if id_player in (id2, id4) and wins != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif id_player in (id1, id3) and wins != 0:
            raise ValueError("Each match loser should have zero wins recorded.")

    print "12. Match can be registered correctly. After a match, players have updated standings."


def testPairings():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerPlayer("Player1", "One", "playerone@tournament.com")
    registerPlayer("Player2", "Two", "playertwo@tournament.com")
    registerPlayer("Player3", "Three", "playerthree@tournament.com")
    registerPlayer("Player4", "Four", "playerfour@tournament.com")
    registerTournament("Tennis")
    registerPlayerToTournament(1, 1)
    registerPlayerToTournament(2, 1)
    registerPlayerToTournament(3, 1)
    registerPlayerToTournament(4, 1)
    standings = playerStandings(1)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(1, id1, id2)
    reportMatch(1, id3, id4)
    pairings = swissPairings(1)
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "13. After one match, players with one win are paired."


def myTest():
    deleteTournaments()
    deleteMatches()
    deletePlayers()
    registerTournament("Hide and seek")
    registerTournament("Wrestling")
    registerPlayer("Player1", "One", "playerone@tournament.com")
    registerPlayer("Player2", "Two", "playertwo@tournament.com")
    registerPlayer("Player3", "Three", "playerthree@tournament.com")
    registerPlayer("Player4", "Four", "playerfour@tournament.com")
    registerPlayer("Player5", "Five", "playerfive@tournament.com")
    registerPlayer("Player6", "Six", "playersix@tournament.com")
    registerPlayerToTournament(1, 1)
    registerPlayerToTournament(2, 1)
    registerPlayerToTournament(3, 1)
    registerPlayerToTournament(4, 1)
    registerPlayerToTournament(5, 1)
    registerPlayerToTournament(6, 1)
    registerPlayerToTournament(5, 2)
    registerPlayerToTournament(6, 2)
    reportMatch(1, 1, 2)
    reportMatch(1, 1, 2)
    reportMatch(1, 7, 2)

    standings = playerStandings(1)
    standings2 = playerStandings(2)


if __name__ == '__main__':
    clearScreen()
    testDeleteTournaments()
    testDeleteMatches()
    testDeletePlayers()
    testCountTournaments()
    testCountMatches()
    testCountPlayers()
    testRegisterTournament()
    testRegisterPlayer()
    testRegisterPlayerToTournament()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    myTest()
    print "\nHooray!  All tests pass!\n"


