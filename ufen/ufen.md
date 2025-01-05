# UFEN
UFEN is a standard notation for describing a particular board position of a game of Ultimate Tic-Tac-Toe. UFEN copies 
the format of FEN (Forsyth–Edwards Notation) for chess, but is adapted for Ultimate Tic-Tac-Toe. The UFEN string should 
be contained in a single line, within a file with a `.ufen` extension. The UFEN string is composed of 3 fields, 
separated by a single space:
1. The board state of the game. Each rank is described from 9 to 1, with a `/` separating ranks. Each square is 
represented from A to I, with `X` indicating a square occupied by player `X`, and `O`. Consecutive empty spaces are 
represented by a number from 1 to 9, indicating how many spaces including the current one are empty. 
2. Active player, either `X` or `O`, indicating that player `X` or player `O` is to move next respectively.
3. The index of the next big board to be played in, from 0 to 9 (left to right, top to bottom). 0 indicates that the
next big board can be any of the 9 big boards, the others are the index of the next big board to be played in starting 
from 1.

# Examples
The following is an example of a UFEN string:  
The starting position of the game:
```
9/9/9/9/9/9/9/9/9 X 0
```  
And after the move 1. `a1`:
```
9/9/9/9/9/9/9/9/X8 O 1
```
And after move 2. `b2`:
```
9/9/9/9/9/9/9/1O7/X8 X 5
```
