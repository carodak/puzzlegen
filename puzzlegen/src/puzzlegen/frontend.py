from puzzlegen.core import Block, GridInitializer, PuzzleLogic, BFSSolver, PuzzleBatchGenerator

class PuzzleGame:
    def __init__(self, nb_blocks, colors, nb_moves, grid_size, stack_probability=0.75, blocks_gap=1):
        """
        Initialize the PuzzleGame frontend.

        Args:
            nb_blocks (int): Number of blocks.
            colors (list): List of colors.
            nb_moves (int): Number of moves to solve.
            grid_size (tuple): (rows, cols) of the grid.
            stack_probability (float): Probability to stack blocks.
            blocks_gap (int): Minimum gap between blocks in a row.
        """
        self.grid = GridInitializer(grid_size, nb_blocks, colors, nb_moves, stack_probability, blocks_gap)
        self.solver = None
        self.solution = None

    def generate_puzzle(self):
        """Generate a new puzzle grid."""
        self.grid.initialize_grid()

    def show_puzzle(self):
        """Display the current puzzle grid."""
        self.grid.print_initial_grid()

    def solve_puzzle(self):
        """Solve the current puzzle and store the solution."""
        self.solver = BFSSolver(self.grid, PuzzleLogic())
        is_solvable, solution = self.solver.perform_all_blocks_moves()
        self.solution = solution if is_solvable else None
        return self.solution

    def save_solution_as_pdf(self, filename):
        """Save the solution as a PDF file."""
        if self.solution:
            BFSSolver.print_history(self.solution, self.grid.grid_size, show=False)
            plt.savefig(filename)
            print(f"Solution saved as {filename}")
        else:
            print("No solution to save.")

    def save_batch_as_csv(self, filename):
        """Save the batch of puzzles as a CSV file."""
        # Suppose you have a batch_generator instance
        if hasattr(self, 'batch_generator'):
            self.batch_generator.save_results_as_csv(filename)
        else:
            print("No batch to save.")


class PuzzleBatch:
    def __init__(self, blocks_range, colors_range, colors_blocks, nb_moves, grid_size, stack_probability=0.75):
        """
        Frontend interface to generate a batch of puzzles.

        Args:
            blocks_range (tuple): (min, max) number of blocks.
            colors_range (tuple): (min, max) number of colors.
            colors_blocks (list): List of possible colors.
            nb_moves (int): Number of moves to solve.
            grid_size (tuple): Grid size (rows, columns).
            stack_probability (float): Probability to stack blocks.
        """
        self.generator = PuzzleBatchGenerator(
            blocks_range, colors_range, colors_blocks, nb_moves, grid_size, stack_probability
        )
        self.generated = False

    def generate(self):
        """Generate the batch of puzzles."""
        self.batch = self.generator.generate_puzzles()
        self.generator.compute_stats()
        self.generated = True

    def show_stats(self):
        """Display batch statistics (bar chart, pie chart)."""
        if self.generated:
            self.generator.print_charts(show=True)
        else:
            print("Batch not generated.")

    def save_pdf(self, filename):
        """Save all batch grids as a PDF file."""
        if self.generated:
            self.generator.print_and_save_batch()
            print(f"PDF saved as {filename}")
        else:
            print("Batch not generated.")

    def save_csv(self, filename):
        """Save batch data as a CSV file."""
        if self.generated:
            self.generator.save_results_as_csv()
            print(f"CSV saved as {filename}")
        else:
            print("Batch not generated.")
