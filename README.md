# Ultimate Tic Tac Toe
This project contains the planned implementation of 3 things: UTTT Bots, UTTT file extensions, and terminal games. The
bots will be implemented with multiple different methods, documented in the `bots` folder. The UTTT file extension is a
simple file format that is used to store UTTT games in a human-readable format, essentially copying the PGN game format
used in chess. We will be able to parse these files, as well as check their validity. Finally, we want to make either a 
python library or a terminal game that allows users to play UTTT against each other or against a bot via that command 
line.

## UTTT Game Handling
Heavy inspiration for the game logic comes from python-chess, a python library that handles chess games, as well as 
Sebastian Lague's Coding Adventure series on YouTube. You can read more about how exactly game logic is implemented in
the respective readme files, as well as the files themselves.

## Bots
The bots will be implemented in the `bots/playable_bots` folder. The bots will be implemented with multiple different 
methods, documented within each bot's file. You can run simulations of the bots playing against each other using the 
`bot_game` or `bot_matchup` files in the `bots` folder.

## UTTT File Extensions
We will be recreating the .pgn and .fen notation used in chess, but for UTTT. The file extensions will be .upgn and .ufen
respectively, and can be inspected in the `upgn` and `ufen` folders. The .upgn file format will store all moves made in
a game, as well as metadata about the game. The .ufen file format will store the current state of the game.