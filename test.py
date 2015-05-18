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
    c = countPlayers()
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
    registerPlayer("Chandra Nalaar", 1)
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1.")
    print "8. After registering a player, countPlayers() returns 1."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    registerPlayer("Markov Chaney", 1)
    registerPlayer("Joe Malik", 1)
    registerPlayer("Mao Tsu-hsi", 1)
    registerPlayer("Atlanta Hope", 1)
    c = countPlayers()
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "9. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Melpomene Murray", 1)
    registerPlayer("Randy Schwartz", 1)
    standings = playerStandings()
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
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "10. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    registerPlayer("Bruno Walton", 1)
    registerPlayer("Boots O'Neal", 1)
    registerPlayer("Cathy Burton", 1)
    registerPlayer("Diane Grant", 1)
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings()
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "11. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle", 1)
    registerPlayer("Fluttershy", 1)
    registerPlayer("Applejack", 1)
    registerPlayer("Pinkie Pie", 1)
    standings = playerStandings()
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    pairings = swissPairings()
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "12. After one match, players with one win are paired."


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
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "\nHooray!  All tests pass!\n"


