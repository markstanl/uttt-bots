# Minimax 1 Bot
This bot employs a simple minimax function with the hueristic evaluation function allegedly based on the Powell-Merrill
paper, but I am unable to find it. But, I was able to locate a comment on [this stackexchange post](https://boardgames.stackexchange.com/questions/49291/strategy-for-ultimate-tic-tac-toe)
that describes the Powell-Merrill algorithm as follows:
```


        1. Winning the game is worth infinity points. Losing the game is worth negative infinity points.
        2. Winning or losing a board results in a gain or loss of 100 points.
        3. If a board is won and it results in two won boards in a row (i.e. winning one more board would result in a won game), then an additional 200 points are added (this may occur multiple times if there are multiple paths to victory).
        4. Winning a board that results in blocking three in a row for the opponent results in 150 points.
        5. Winning a board that is already blocked by the opponent’s boards results in -150 points.
        6. Making two marks in a row on a small board adds 5 points
        7. Blocking an opponent win on a small board adds 20 points
        8. Making a move in a board that has no benefit to the player subtracts 20 points

```