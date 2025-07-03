# puzzlegen

**Procedural Match-3 Puzzle Generator and Solver**  
Developed by Caroline DAKOURE

---

## Overview

`puzzlegen` is a Python package for generating, visualizing, and solving procedural Match-3 puzzles, designed for cognitive science and executive functioning tasks.  
It allows you to create single puzzles or batches, visualize them, and automatically find solutions using a Breadth-First Search (BFS) solver.

<img src="https://github.com/carodak/puzzlegen/blob/main/doc/puzzle-gen.png">
---

## Features

- **Random puzzle generation** with customizable grid size, colors, and block counts
- **Automatic solver** (BFS) to check puzzle solvability within a given number of moves
- **Batch generation**: create and filter many puzzles at once
- **Visualization**: display puzzles and solutions as images or PDFs
- **Export**: save puzzles and solutions as PDF or CSV

---

## Installation

```bash
pip install matplotlib
# Or, if you want to install from source:
git clone https://github.com/carodak/puzzlegen.git
cd puzzlegen
pip install .
```

---

## Basic Usage
For detailed usage examples, please see:

`examples/basic_usage.py`

This script demonstrates how to generate, solve, and save puzzles using the `puzzlegen` package.

---

## Puzzle Rules

1. **Puzzle Setup**: The game board is a grid with colored blocks. Blocks are initially placed in the last row or stacked on top of each other. No more than 2 blocks of the same color are aligned horizontally or vertically. Each color must have at least 3 blocks.
2. **Game Play**: The goal is to remove all blocks from the grid in as few moves as possible.
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

MIT License

---

**Contact:**  
caroline.dakoure@umontreal.ca