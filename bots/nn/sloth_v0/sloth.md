# Sloth Bot

The sloth U3T bot which attempts to reapply ideas from the landmark chess bot 'Girrafe', you can read the
paper [here](https://arxiv.org/pdf/1509.01549). The bot is named to call reference of this paper, and also because 
sloths are cool. Like Giraffe, Sloth uses an MLP to evaluate the position.

## Monte Carlo Tree Search
[Wiki](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search)  
There are many ways of evaluating a position. In chess, you can run a static evaluation function, with a minimax search
to figure out how good a position is. Despite multiple attempts, there is no conventional way to evaluate a U3T
position. Thus, we look for another way. Were we to randomly play out the game from a given position, we could determine
the number of wins losses and draws from that position. The assumption is that the more wins we have, the better the
position is. This is the basis of Monte Carlo Tree Search (MCTS).

## Differences
The main difference between Giraffe and Sloth is the input tensor. Giraffe has an interesting input tensor, which is 
based on a lot of metadata from the chess game itself. Sloth, on the other hand, has a much simpler input tensor. It is
just made of the subgame X and O bitboards, as well as a bitboard for the next legal moves.

