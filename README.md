# What is it?

A JupyterLab script I created for randomly generating match-3 puzzles that respect the rules below. I implemented a BFS Solver. Created for CRISPLab. Procedural Content Generation (PCG).

# Quick Overview
  <img src="https://github.com/carodak/Puzzle-Generation/blob/main/doc/puzzle-gen.png">

# Rules


    1.Puzzle Setup: The game board has a grid with colored blocks arranged in a specific pattern.
    The blocks are initially located in the last row of the grid, either alone or on top of another block.
    There are no blocks that end up without a block beneath them (except for the last row of the grid).
    No more than 2 blocks of the same color are horizontally or vertically aligned. Each colour must have at least 3 blocks.
    2.Game Play: The player's goal is to remove all blocks from the grid in as few moves as possible.
    3.Available Moves:
        a. Simple Move: The player can move a block one cell to the left or right if the target cell is empty.
        b. Exchange: The player can swap a block with the one to its left or right, if the target cell is occupied.
    4.Elimination Rule: If more than 2 blocks of the same color are aligned horizontally or vertically, then all aligned blocks disappear.
    5.Falling Rule: If there is no block beneath a block, then the block falls until it is supported by another block or it reaches the bottom row of the grid.
    6.Winning Condition: The player wins when all blocks are removed from the grid in a minimum number of moves. Wrong moves can cause the player to fail to clear all the blocks.