# UTTTAI Conversion

[UTTTAI](https://github.com/markstanl/utttai) is another attempt (and a better one at that) at making an AI that can
play
U3T. They provide the dataset that is used to train out models. But, their internal implementation of game stat
differs from how we understand it. For convenience, we will call our project `U3T`, and their project `UTTTAI`. The
dataset on hugging face that we have altered generally keeps the general data structure that UTTAI uses, but with
reworked standard conventions for indices.  
  
The `utttai_convert` module contains the functions to convert between the two formats, specifically, it reformats the
data to more standard u3t conventions, which will be described below.

## U3T Logic

Our game stores 6 bitboards, 2 for each X, O, and any presence on the small tile bitboard, and the supergame big
bitboard, with the least significant bit referring to the lowest index (bottom left), moving rightward and upward until
the msb is the top right bit.

## UTTTAI Logic

UTTTAI stores all of their data in a single length 93 bytearray. The following is how it is implemented

```
byte_array = / "subgames" (small board) / "supergames" (big board) / current player / constraint /  result
                    (81 bytes)                  (9 bytes)               (1 byte)       (1 byte)    (1 byte)
```

Where a 1 is an X, a 2 is an O. The "constraint" represents the next board to be played in (0-8) or t for any, and
the result for a win is the X or O value, and a draw is 3. They also follow the lsb lowest index to msb highest index
convention.

## Key differences

UTTTAI initially dictates rows and columns via indices 0-8, as opposed to the classical algebraic notation.
The indices of a move are completely different between the two versions. U3T employs the standard chess-style approach
for indices (as seen from [chess-programming](https://www.chessprogramming.org/0x88)
or [bitboard beginnings](https://pages.cs.wisc.edu/~psilord/blog/data/chess-pages/rep.html). UTTTAI, on the other hand,
starts with 0 in the top left corner, and proceeds in what I will call row-big tile
order, by proceeding rightward down the row until it would hit a new supergame, then just proceeding down the row in the
current big tile. You can see the differences in the following images.

### UTTAI Board

![UTTTAI Board](/assets/utttai.png)

### U3T Board

![U3T Board](/assets/num.png)

This applies the same to the indices of the superboards (big boards). Consider:

### UTTTAI Superboard

![UTTTAI](/assets/utttai_big.png)

### U3T Superboard

![U3T](/assets/num_big.png)

UTTTAI definitely employs some non-conventional practices, but it creates a darn good AI model. So we will be fixing up
the dataset to follow some more traditional conventions.

## Conversion

A dictionary lookup is quicker, which you cna find in the `utttai_conversion` init file, but use the following formulas
to convert between the two indices.

### From UTTTAI to U3T

```
u3t_tile_index = 27 * (2 - (index // 27)) + 9 * (2 - ((index // 3) % 3)) + (index % 3) + 3 * ((index // 9) % 3)
```

### From U3T to UTTTAI

```
utttai_tile_index = 9 * (2 - (index // 9)) + 3 * (2 - ((index // 3) % 3)) + (index % 3) + 3 * ((index // 27) % 3)
```

## Updated Format
```
byte_array = / "subgames" (small board) / "supergames" (big board) / current player / constraint /  result
                    (81 bytes)                  (9 bytes)               (1 byte)       (1 byte)    (1 byte)
```
The subgames and supergames byte array now follows the u3t convention, as shown in the images above, with the lsb 
matching to the lowest index. The constraint byte also follows the big board index convention of u3t. The result and
current player bytes remain the same. 

### UTTTAI Justification

I have likely been a little harsh in my analysis of UTTTAI's indexing. Though it is unconventional for chess, there is a
good justification for it for U3T specifically. Having all subgames in a single row allows for a more easily understood
tic-tac-toe mask arrays (this is how the bot knows if there has been a tic tac toe in a subgame). This is absolutely 
one of the downsides of the conventional bitboards for chess, as the mask arrays are significantly less intuitive.
Furthermore, there is great value in using bytearrays as opposed to bitboards, as it is easy to see the entire data 
of a game stored in a single array.