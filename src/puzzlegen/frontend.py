from puzzlegen.core import GridInitializer, PuzzleLogic, BFSSolver, PuzzleBatchGenerator

class SinglePuzzle:
    """
    User-facing interface for generating and solving a single Match-3 puzzle instance.
    Wraps the core logic to provide a simplified API.
    """
    def __init__(self, nb_blocks, colors, nb_moves, grid_size, stack_probability=0.75, blocks_gap=1):
        """
        Initialize the SinglePuzzle frontend.

        Args:

            nb_blocks (int): Total number of blocks to place on the grid.

            colors (list of str): List of colors to use for the blocks.

            nb_moves (int): Upper bound on the number of moves in the optimal solution. The generator ensures the puzzle can be solved in at most this number of moves.

            grid_size (tuple of int): Dimensions of the grid as (rows, columns).

            stack_probability (float, optional): Probability of stacking blocks vertically. Default is 0.75.
            
            blocks_gap (int, optional): Maximum allowed gap between blocks during generation (e.g., 1 means at most one empty cell). Default is 1.
        """
        self.grid = GridInitializer(grid_size, nb_blocks, colors, nb_moves, stack_probability, blocks_gap)
        self.solver = None
        self.solution = None

    def generate(self):
        """Randomly generate a puzzle grid based on the parameters defined in the SinglePuzzle instance."""
        self.grid.initialize_grid()

    def show(self):
        """Display the initial state of the puzzle grid."""
        self.grid.print_initial_grid()

    def solve(self):
        """
        Attempt to solve the puzzle using BFS. The search is limited to solutions within a maximum number of moves (`nb_moves`).

        Returns:
            solution (dict or None): 
                A dictionary containing the move history and block states leading to the solution,
                or None if no solution exists within `nb_moves` (meaning the solution requires more moves).
        """
        self.solver = BFSSolver(self.grid, PuzzleLogic())
        is_solvable, solution = self.solver.perform_all_blocks_moves()
        self.solution = solution if is_solvable else None
        return self.solution
    
    def show_solution(self):
        """Display the solution path if one was found."""
        if self.solution:
            BFSSolver.print_history(self.solution, self.grid.grid_size, show=True)
        else:
            print("No solution found.")

class PuzzleBatch:
    """
    Frontend interface for generating and exporting multiple puzzles with varying parameters.
    Useful for statistical analysis or dataset creation.
    """
    def __init__(self, blocks_range, colors_range, colors_blocks, nb_moves, grid_size, nb_attempts = 5, stack_probability=0.75, blocks_gap=1):
        """
        Initialize the batch puzzle generator.

        Args:

            blocks_range (tuple of int): Range of block counts to iterate over as (min_blocks, max_blocks).
                For each block count in this range, puzzles will be generated.
            
            colors_range (tuple of int): Range of color counts to iterate over as (min_colors, max_colors).
                For each color count in this range, puzzles will be generated.

            colors_blocks (list of str): Pool of possible block colors to choose from.

            nb_moves (int): Maximum number of moves allowed in the optimal solution.
                The generator attempts to create puzzles solvable within this limit.

            grid_size (tuple of int): Dimensions of the puzzle grid as (rows, columns).

            nb_attempts (int, optional): Number of attempts to generate a solvable puzzle for each
                combination of blocks and colors. If no valid puzzle is found after these attempts,
                no puzzle is generated for that combination. Default is 5.

            stack_probability (float, optional): Probability to stack blocks vertically during generation.
                Default is 0.75.
            blocks_gap (int, optional): Maximum allowed gap between blocks during generation (e.g., 1 means at most one empty cell). Default is 1.
        """
        self.generator = PuzzleBatchGenerator(
            blocks_range, colors_range, colors_blocks, nb_moves, grid_size, nb_attempts, stack_probability, blocks_gap
        )
        self.generated = False

    def generate(self):
        """Generate a batch of puzzles based on the configured parameter ranges."""
        self.batch = self.generator.generate_puzzles()
        self.generator.compute_stats()
        self.generated = True

    def show_stats(self):
        """Display statistical charts for the generated batch (e.g., bar chart and pie chart)."""
        if self.generated:
            self.generator.print_charts(show=True)
        else:
            print("Batch not generated.")

    def save_pdf(self, filename):
        """
        Export all puzzle grids in the batch as a PDF.

        Args:
            filename (str): Output filename for the PDF.
        """
        if self.generated:
            self.generator.print_and_save_batch(filename=filename)
            print(f"PDF saved as {filename}")
        else:
            print("Batch not generated.")

    def save_csv(self, filename):
        """
        Export puzzle metadata and configuration results as a CSV file.

        Args:
            filename (str): Output filename for the CSV.
        """
        if self.generated:
            self.generator.save_results_as_csv(filename=filename)
            print(f"CSV saved as {filename}")
        else:
            print("Batch not generated.")
