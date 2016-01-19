# Project 2 - "Swiss Tournament"
## Udacity's Full Stack Developer Nanodegree 

## Instructions:

* Use the `tournament.sql` to create your database and its tables.
* `tournament.py` holds the Python code needed to organize a Swiss-style tournament.
  - Note that this version requires an even number of players (no byes will be given).
* The original `tournament_test.py` can be run to check that all the functions will run properly.
* The files `mytest.py` and `myTest_Tie.py` give a full simulation of a tournament (with and without ties respectively).

###Things to Note

* Ties are possible though the default in match reporting is there are only winners and losers (no ties). A match can be reported as a tie by calling `reportMatch(player1,player2,tie=True)`. A player who ties gets 1 point.
* To allow for tie scoring, the point allocation had to be changed so that a win counts for **3 points**, a lost counts for **0 points** and a tie counts for **1 point**. If no ties are given, the points can be reverted to the original allocation (1 point for a win and 0 points for a lost) by dividing the players' scores/standings by 3.
