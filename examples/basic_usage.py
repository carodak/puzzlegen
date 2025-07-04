# ----------------------------------------------------------
# Puzzle Generation Code for the Executive Functioning Task (https://osf.io/3pz74/wiki/home/)
# Developed by Caroline DAKOURE
# ----------------------------------------------------------

from puzzlegen.frontend import SinglePuzzle, PuzzleBatch

# ----------------------------------------------------------
# Example 1: Randomly generate and solve a single puzzle
# ----------------------------------------------------------

# 1. Instantiate a single puzzle
puzzle = SinglePuzzle(nb_blocks=10, colors=['red', 'blue', 'gray'], nb_moves=5, grid_size=(12, 12))

# 2. Generate the puzzle grid randomly
puzzle.generate()

# 3. Display the puzzle
puzzle.show()

# 4. Attempt to solve the puzzle (i.e., find a solution within nb_moves)
solution = puzzle.solve()

# 5. Save the solution and batch as files
puzzle.show_solution()

# ----------------------------------------------------------
# Example 2: Generate a batch of puzzles
# ----------------------------------------------------------

# In this process, puzzles that cannot be solved within the specified maximum number of moves (nb_moves)
# are automatically discarded. Only puzzles solvable in nb_moves moves or fewer are kept.

# 1. Instantiate a batch of puzzles
batch = PuzzleBatch(
    blocks_range=(6, 10),
    colors_range=(2, 4),
    colors_blocks=['blue', 'red', 'gray'],
    nb_moves=5,
    grid_size=(12, 6),
    nb_attempts=3,
    stack_probability=0.75
)

# 2. Generate the batch
batch.generate()

# 3. Show statistics and save the results
batch.show_stats()
batch.save_pdf("batch_puzzles.pdf")
batch.save_csv("batch_puzzles.csv")
