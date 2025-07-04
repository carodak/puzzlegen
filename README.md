# puzzlegen - Procedural Match-3 Puzzle Generator 
Developed by Caroline DAKOURE

**Project Links:**  
[GitHub Repository](https://github.com/carodak/puzzlegen/) | [PyPI Project](https://pypi.org/project/puzzlegen/) | [OSF Project](https://doi.org/10.17605/OSF.IO/HNAQ9)

## Overview

`puzzlegen` is a Python package for generating, visualizing, and solving procedural Match-3 puzzles.
It allows you to create single puzzles or batches, visualize them, and automatically find solutions using a Breadth-First Search (BFS) solver.

<img src="https://raw.githubusercontent.com/carodak/puzzlegen/refs/heads/main/docs/assets/puzzle-gen.png">

---

## Features

- **Random puzzle generation** with customizable grid size, colors, and block counts
- **Automatic solver** (BFS) to check puzzle solvability within a given number of moves
- **Batch generation**: create and filter many puzzles at once
- **Visualization**: display puzzles and solutions as images or PDFs
- **Export**: save puzzles and solutions as PDF or CSV

---

## Installation

### Option 1
```bash
pip install puzzlegen
```

### Option 2
Or, if you want to install from the github repository that may contain more up-to-date versions:
```bash
pip install git+https://github.com/carodak/puzzlegen.git
```

### Option 3
Or, if you want to clone and install locally:
```bash
git clone https://github.com/carodak/puzzlegen.git
cd puzzlegen
pip install .
```

---

## Basic Usage

### Example 1: Randomly generate and solve a single puzzle
```bash
from puzzlegen.frontend import SinglePuzzle

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
```

### Example 2: Generate a batch of solvable puzzles
```bash
from puzzlegen.frontend import PuzzleBatch

# 1. Set up a batch generator with parameter ranges
batch = PuzzleBatch(
    blocks_range=(6, 10),
    colors_range=(2, 4),
    colors_blocks=['blue', 'red', 'gray'],
    nb_moves=5,
    grid_size=(12, 6),
    stack_probability=0.75
)

# 2. Attempt to generate solvable puzzles for all combinations within the given ranges
batch.generate()

# 3. Show stats and save the results
batch.show_stats()
batch.save_pdf("batch_puzzles.pdf")
batch.save_csv("batch_puzzles.csv")
```

### Or use without installation
You can also use the package directly in the Jupyter notebook located at `examples/basic_usage.ipynb`, available online here: https://colab.research.google.com/github/carodak/puzzlegen/blob/main/examples/basic_usage.ipynb — no installation needed.

### For additional detailed usage examples, please see:

`examples` folder

This script demonstrates how to generate, solve, and save puzzles using the `puzzlegen` package.

---

## Puzzle Rules

1. **Puzzle Setup**: The game board is a grid with colored blocks. Blocks are initially placed in the last row or stacked on top of each other. No more than 2 blocks of the same color are aligned horizontally or vertically. Each color must have at least 3 blocks.
2. **GamePlay**: The goal is to remove all blocks from the grid in as few moves as possible.
3. **Available Moves**:
    - *Simple Move*: Move a block left or right if the target cell is empty.
    - *Exchange*: Swap a block with its left or right neighbor if the target cell is occupied.
4. **Elimination Rule**: If 3 or more blocks of the same color are aligned horizontally or vertically, they disappear.
5. **Gravity Rule**: Blocks fall down if unsupported until they reach another block or the bottom of the grid.
6. **Winning Condition**: All blocks are removed from the grid within the allowed number of moves.

Executive Function Task Reference: https://osf.io/3pz74/wiki/home/

---

## Project Structure

- `src/puzzlegen/core/` – Core logic (puzzle generation, solver, batch processing, etc.)
- `src/puzzlegen/frontend.py` – User-friendly interface for puzzle creation and batch operations
- `examples/` – Example notebooks and scripts to help you get started
- `tests/` – Unit tests for code reliability
- `outputs/` – Folder where generated puzzles and results are saved

---

## API Documentation

The API Documentation is available at https://carodak.github.io/puzzlegen/puzzlegen.html or in `docs` folder.

---

## Contributing

Pull requests and suggestions are welcome!  
Please add tests for any new features.

---

## Resources

- [Solving simplified Candy Crush (Medium)](https://medium.com/swlh/solving-simplified-candy-crush-i-e-match-3-games-with-swaps-54cb7975486b)
- [EightPuzzle (GitHub)](https://github.com/MohamadTarekk/EightPuzzle)
- [BFS explanation (YouTube)](https://www.youtube.com/watch?v=MQ-BffUgYfM)
- [Visualgo BFS/DFS](https://visualgo.net/en/dfsbfs)
- [What is BFS? (dev.to)](https://dev.to/lukegarrigan/what-is-bfs-breadth-first-search-nad)

---

## License

GPL-3.0

---

**Contact:**  
caroline.dakoure@umontreal.ca