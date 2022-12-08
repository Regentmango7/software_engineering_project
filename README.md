# SOFTWARE ENGINEERING PROJECT FOR CSDS393 By JD Tramonte and Paul Schussler

This project is an incremental clicker game set in the mines.
The way it works is that the player will click in the center circle to generate ores. The types of ores generated depends on the mines
These ores can be sold for coins in the smithing tab. coins can be used to purchase new mines, or buy miners to automate clicking for you
Miners can be assigned to different mines, and unassigned
Upgrades cost raw ores to purchase
Contracts take a certain ore type, and will return much more cash for them than normal
The stats page contains all the different statistics for the player
The guilds page contains different disciplines the player can aquire. Each discipline requires a threshold, which is a certain amount of total coins that a player has gathered in this retirement/run (explained below). Only one discipline per row can be aquired at a time. 
The Miner On Click discipline gives a miner to the player on each click. The Drop Rate discipline fixes the drop rate so that each mine will only drop the most profitable ore. The Click Multiplier discipline will multiply the clicks by the amount of miners a player has. The Sell Rate discipline will massivly increase how much an ore will sell for.
The retirement page takes the entirety of a player's accomplishments, and converts it into skill points than can be spent on exclusive upgrades. This means that the player is reset back to zero, but can aquire new and powerful upgrades that will stick with them across retirements/runs

<br>

# How to Run

You can run the Click Miners game by cloning the repo and then calling the following on your command line:

```
py {path}/miner_game.py
```
