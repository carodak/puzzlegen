# ----------------------------------------------------------
# Puzzle Generation Code for the Executive Functioning Task (https://osf.io/3pz74/wiki/home/)
# Developed by Caroline DAKOURE
# ----------------------------------------------------------

from puzzlegen.frontend import SinglePuzzle, PuzzleBatch

# ----------------------------------------------------------
# Example 1: Randomly generate and solve a single puzzle
# ----------------------------------------------------------

# 1. Create a single puzzle with defined parameters
puzzle = SinglePuzzle(nb_blocks=10, colors=['red', 'blue', 'gray'], nb_moves=5, grid_size=(12, 12))

# 2. Randomly populate the puzzle board with blocks
puzzle.generate()

# 3. Visualize the puzzle
puzzle.show()

# 4. Try to solve the puzzle (within the allowed number of moves)
solution = puzzle.solve()

# 5. Visualize the solution (if found)
puzzle.show_solution()

# ----------------------------------------------------------
# Example 2: Generate a batch of puzzles
# ----------------------------------------------------------

# In this process, puzzles that cannot be solved within the specified maximum number of moves (nb_moves)
# are automatically discarded. Only puzzles solvable in nb_moves moves or fewer are kept.

# 1. Set up a batch generator with parameter ranges
batch = PuzzleBatch(
    blocks_range=(6, 10),
    colors_range=(2, 4),
    colors_blocks=['blue', 'red', 'gray'],
    nb_moves=5,
    grid_size=(12, 6),
    nb_attempts=3,
    stack_probability=0.75
)

# 2. Attempt to generate solvable puzzles for all combinations within the given ranges
batch.generate()

# 3. Show stats and save the results
batch.show_stats()
batch.save_pdf("batch_puzzles.pdf")
batch.save_csv("batch_puzzles.csv")
