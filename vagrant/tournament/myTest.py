from tournament import *
from random import random as rand

deleteMatches()
deletePlayers()

# Inputs
numPlayers = 16
rounds = 4

# Register Players
for i in range(numPlayers):
    registerPlayer("Player %2d" %(i+1))

s = [playerStandings()]
ids = [0]+ [x[0] for x in s[0]]
pairs =[]


# Play the rounds
for temp in range(rounds+1):
    pairs += [swissPairings()]
    # Random winners and losers
    for x in pairs[temp]:
      i = 1 if rand() > 0.5 else 0
      # Report w/ ids
      reportMatch(x[i*2],x[2*((i+1)%2)])
    s += [playerStandings()]

# Report rounds
for x in range(rounds+1):
    ss = s[x]
    ss.sort(key=lambda l: l[2], reverse=True)

    for p in ss:
        print "%s (%d) with %d wins after %d rounds" %(p[1],p[0],p[2],p[3])
    print "\n\n"
    for pair in pairs[x]:
        print "%s vs %s" %(pair[1],pair[3])
