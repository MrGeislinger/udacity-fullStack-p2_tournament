#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

# Default tournamentID
#TOURNMENTID = 0;

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    # Delete players from registration and standings
    c.execute("DELETE FROM rounds;")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    #
    conn = connect()
    c = conn.cursor()
    # Delete players from registration and standings
    c.execute("DELETE FROM  standings;")
    c.execute("DELETE FROM registeredPlayers;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    #
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM registeredPlayers;")
    count = c.fetchone()[0]
    conn.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    #
    conn = connect()
    c = conn.cursor()
    # Register player into tournament
    c.execute("INSERT INTO registeredPlayers (name) VALUES (%s) RETURNING id;", (name,))
    playerId = c.fetchone()[0]
    conn.commit()
    # Add the player to standings (no wins, no matches)
    c.execute("INSERT INTO standings (player) VALUES (%d);" %(playerId))
    conn.commit()
    conn.close()


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

    conn = connect()
    c = conn.cursor()
    c.execute('''SELECT id, name, points, matches
        FROM standings, registeredPlayers
        WHERE standings.player = registeredPlayers.id
        ORDER BY points;
    ''')
    standings = c.fetchall()
    conn.commit()
    conn.close()
    return standings

def updateStandings(player, matchOutcome):
    """Updates a player's standing after a match.

    Args:
        player:  the id number of the player whose stats are being updated
        matchOutcome: outcome of match (possible values: "won", "lost", "tie")
    """

    # Default to no points if "lost" or other unrecognized `matchOutcome`
    points = 0
    if(matchOutcome == "won"):
        points = 3
    elif(matchOutcome == "tie"):
        points = 1

    conn = connect()
    c = conn.cursor()
    # Assume another match was played
    command = "UPDATE standings SET matches = matches + 1, points = points + %.1f " %(points)
    # Avoid string interpolation on `player` (no SQL injection)
    command += "WHERE standings.player = %s;"
    c.execute(command, (player,))
    conn.commit()
    conn.close()

def reportMatch(winner, loser, tie=False):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tie: whether the players tied (boolean value); default is `False`
    """

    # Use helper function to more cleanly update table
    # Helper function accesses/updates table once (total of two times here)
    if(not tie):
        updateStandings(winner,"won")
        updateStandings(loser,"lost")
    else:
        updateStandings(winner,"tie")
        updateStandings(loser,"tie")

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

    # Get players standings (not neccessarily sorted)
    players = playerStandings()
    # Put into descending order wins/points (ensures winners are matched 1st)
    players.sort(key=lambda l: l[2], reverse=True)
    # Create a list of tuples (id1, name1, id2, name2) based on wins/points
    pairs = []
    for i in range(len(players)/2):
        # Get one pair at a time; player is (id, name)
        pairs += [(players[i*2][:2] + players[i*2+1][:2])]
    return pairs
