# "Watch Your Back" Game Playing AI
Authors: Ckyever Gaviola, Samuel Fatone

## Game Rules
See game-spec-2018.pdf

## Project Overview
### watchyourback.py:
This module contains our Board and Piece class which allow us to create an
internal representation of "Watch Your Back!". It contains functions which
handle game events such as the placing, moving, elimination of pieces and
shrinking of the board. Most notably we've added the ability to undo piece
placing and moving (inspired by sample solution) to use in our search algorithms
rather than creating copies of board states to construct a tree.

### minimax_module.py:
Contains the Player class with the required functions indicating in the
assignment spec. It also includes an evaluation function for the game board and
seperate search algorithm functions for the moving and placing phase.

### random_module.py:
Similar to minimax_module.py but makes moves/places at random. Was used as a
test opponent and the evaluation function was tweaked to optimise its
performance to play against this player.

### Search strategy:
We've attempted to implement a basic minimax search algorithm with alpha-beta
pruning. Both placing and moving strategies utilise a wrapper function which
records all the possible moves given the current board state when it was called
and its corresponding minimax value. We obtain these minimax values by first
making the move, recursively calling the min max functions, then undoing the
move. The max and min functions would recursively call each other to simulate
our player (MAX) taking a turn and then our opponent (MIN) taking a turn until
passing the specified cutoff test (base case) where it would return the utility
value of the board via the evaluation function.
Another strategy we have implemented attempts to get all of the player pieces
away from the border when it is near shrinking. To do this, we added functions
to count the number of player pieces that are on the border, which in turn
enables us to know at which move we should start moving them to a more central
position. Using these functions should enable all of the player pieces to
escape being killed by the border shrink.
When deciding on a move, the border functions are examined first to decide
whether the border pieces have to be moved to escape death. However, if the
pieces do not have to be moved just yet, the minimax algorithm above is used
instead.

### Evaluation function:
The heuristic we've chosen here is the number of our pieces relative to the
opponents pieces currently alive on the board. We increment the value for each
of our pieces and decrement it for each of our opponents pieces. We've decided
to give our own pieces greater weight compared to enemy pieces to encourage
a defensive strategy where minimax would favour moves that keeps its pieces
alive rather than eliminating enemy pieces. We've also combined that with the
Manhattan distance of our pieces from the centre of the board which reduces the
value the further they are from the middle. From playing games and running
simulations it is apparent that controlling the middle is vital since games tend
to run till after the second shrink and it is best to avoid being eliminated
by them. Although this was weighted less than having a greater number of pieces
on the board.

### Issues:
The current implementation of our search strategy is not the correct use of
minimax search and the player sometimes makes invalid moves when playing as
black. We believe it is caused due to our minimax function during the moving
phase manipulating our representation of the board. The wrapper functions should
be calling min_place/move(MOVE_DEPTH, inf, -inf) since it has already made a
move/place for MAX. Also the search time dramatically increases when we increase
the current search depths (to a point where it may go over the time limit). Our
attempts at fixing these issues resulted in even worse performance which is
why we've submitted as is.
