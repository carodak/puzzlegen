import datetime
import csv
import os
from matplotlib.backends.backend_pdf import PdfPages

class PuzzleBatchGenerator:
    """
    Generates and manages batches of puzzles with varying parameters.

    This class allows you to:
      - Generate multiple puzzles for different combinations of block counts and color counts.
      - Automatically filter out unsolvable puzzles (within the specified number of moves).
      - Collect statistics on solvable/unsolvable puzzles.
      - Save results as PDF (visuals) and CSV (data).
      - Display summary charts (bar and pie charts) of the batch.

    Args:
        blocks_range (tuple): (min, max) number of blocks per puzzle.
        colors_range (tuple): (min, max) number of colors per puzzle.
        colors_blocks (list): List of possible colors.
        nb_moves (int): Maximum number of moves allowed to solve a puzzle.
        batch_grid_size (tuple): Grid size for each puzzle (rows, columns).
        batch_stack_probability (float): Probability to stack blocks during generation.

    Attributes:
        puzzle_batch (dict): Stores generated puzzles, grouped by number of moves to solve.
        nb_solvables (int): Number of solvable puzzles generated.
        nb_unsolvables (int): Number of unsolvable puzzles generated.
        stats (dict): Statistics on the batch (number of puzzles per move count).
        csv_data (dict): Data for CSV export.
    """

    def __init__(self, blocks_range, colors_range, colors_blocks, nb_moves, batch_grid_size, batch_stack_probability):
        self.blocks_range = blocks_range
        self.colors_range = colors_range
        self.colors = colors_blocks
        self.nb_moves = nb_moves
        self.puzzle_batch = {}
        self.nb_solvables = 0
        self.nb_unsolvables = 0
        self.stats = {}
        self.csv_data = {}
        self.batch_grid_size = batch_grid_size
        self.batch_stack_probability = batch_stack_probability

    def generate_puzzles(self):
        """
        Generate a batch of puzzles for all combinations of block and color counts.

        For each combination:
          - Tries up to 5 times to generate a solvable puzzle.
          - Stores puzzles by the number of moves required to solve.
          - Updates statistics and CSV data.

        Returns:
            dict: The generated batch of puzzles, grouped by moves required to solve.
        """
        iterated_colors = []
        puzzle_batch = {}
        csv_data = {
            "cubes": [],
            "positions": [],
            "colors": [],
            "moves": []
        }
        stack_probability = self.batch_stack_probability
        blocks_gap = 1

        for i in range(1, nb_moves+1):
            key = 'solvable_in_' + str(i) + '_moves'
            puzzle_batch[key] = []

        for nb_colors in range(self.colors_range[0], self.colors_range[1] + 1):
            iterated_colors = self.colors[:nb_colors]
            for nb_blocks in range(self.blocks_range[0], self.blocks_range[1]+1):
                if len(iterated_colors)*3 > nb_blocks:
                    #print('Not enough blocks for the number of colors. You need at least 3 blocks per color.')
                    continue
                else:
                    if nb_colors == 1:
                        grid_size = (nb_blocks+1, nb_blocks+1)
                    else:
                        grid_size = self.batch_grid_size
                    is_solvable = False
                    print(f"Generating puzzle for {nb_blocks} blocks, {iterated_colors} colors. The size of the grid is: {grid_size}.")
                    nb_attempts = 0
                    while not(is_solvable) and nb_attempts < 5:
                        grid = GridInitializer(grid_size, nb_blocks, iterated_colors, self.nb_moves, stack_probability, blocks_gap)
                        grid.initialize_grid()
                        solver = BFSSolver(grid, PuzzleLogic())
                        is_solvable, solution = solver.perform_all_blocks_moves()
                        nb_attempts = nb_attempts + 1
                    if is_solvable:
                        round = solution["rounds_number_history"][-2]
                        key = 'solvable_in_' + str(round) + '_moves'
                        puzzle_batch[key] = puzzle_batch[key] + [(solution, grid_size)]

                        positions_list = []
                        colors_list = []

                        init_pos = solution['set_blocks_history'][0]
                        for position, block in init_pos.items():
                            positions_list.append(position)
                            color = block.get_color()
                            colors_list.append(color)

                        csv_data["cubes"] = csv_data["cubes"] + [nb_blocks]
                        csv_data["colors"] = csv_data["colors"] + [colors_list]
                        csv_data["positions"] = csv_data["positions"] + [positions_list]
                        csv_data["moves"] = csv_data["moves"] + [round]
                        self.nb_solvables = self.nb_solvables + 1
                    else:
                        self.nb_unsolvables = self.nb_unsolvables + 1

        self.puzzle_batch = puzzle_batch
        self.csv_data = csv_data
        print("Batch generation completed.")
        return self.puzzle_batch



    def print_and_save_batch(self):
        """
        Print and save all generated puzzles as a PDF file.

        - Visualizes each puzzle's solution history.
        - Saves all figures to a single PDF.
        - Also displays summary charts (bar and pie).
        """
        for move in sorted(self.puzzle_batch.keys()):
          list_solved_puzzles = self.puzzle_batch[move]
          for i in range(len(list_solved_puzzles)):
            solved_puzzle = list_solved_puzzles[i][0]
            grid_size = list_solved_puzzles[i][1]
            #print(f"This is the list of puzzles generated for: {move}")
            BFSSolver.print_history(solved_puzzle, grid_size, False)
        self.print_charts(False)
        filename = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")+'_puzzle_generation.pdf'
        self.save_multi_image(filename)

    def save_multi_image(self, filename):
        """
        Save all open matplotlib figures to a single PDF file.

        Args:
            filename (str): Name of the PDF file to save.
        """
        pp = PdfPages(filename)
        fig_nums = plt.get_fignums()
        figs = [plt.figure(n) for n in fig_nums]
        for fig in figs:
          fig.savefig(pp, format='pdf')
        pp.close()
        self.save_file(filename)
        plt.show()

    def compute_stats(self):
        """
        Compute statistics for the generated batch.

        Populates the `stats` attribute with the number of puzzles solvable in each move count.
        """
        for move in sorted(self.puzzle_batch.keys()):
          self.stats[move] = len(self.puzzle_batch[move])
        print("stats: ", self.stats)

    def set_batch(self, batch):
        """
        Set the current batch of puzzles.

        Args:
            batch (dict): Batch of puzzles to set.
        """
        self.puzzle_batch = batch

    def print_charts(self, show):
        """
        Display bar and pie charts summarizing the batch statistics.

        Args:
            show (bool): If True, displays the charts.
        """
        labels = list(self.stats.keys()) + ['unsolvable']
        sizes = list(self.stats.values()) + [self.nb_unsolvables]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        ax1.bar(labels, sizes)
        ax1.set_title('Number of Puzzles Generated (Bar Chart)')

        ax2.pie(sizes, labels=labels, autopct=lambda p: '{:.2f}%({:.0f})'.format(p,(p/100)*sum(sizes)))
        ax2.set_title('Number of Puzzles Generated (Pie Chart)')

        fig.tight_layout()

        if show:
          plt.show()

    def save_results_as_csv(self):
        """
        Save the batch data as a CSV file.

        The CSV contains, for each puzzle:
          - Number of blocks
          - Colors used
          - Initial positions
          - Number of moves to solve

        The file is saved with a timestamp in the filename.
        """
        filename = str(datetime.datetime.now()) + '_puzzle_generation.csv'
        fieldnames = list(self.csv_data.keys())
        with open(filename, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(self.csv_data["cubes"])):
                writer.writerow({fieldname: self.csv_data[fieldname][i] for fieldname in fieldnames})
        self.save_file(filename)


    def save_file(self, filename):
        """
        Save a file either locally (in 'outputs' folder) or download in browser if running in Jupyter/Colab.

        Args:
            filename (str): Name of the file to save.
        """
        if 'google.colab' in str(get_ipython()):
            from google.colab import files
            files.download(filename)
            print("Looks like we are on google colab so we file would be saved on our Kernel")
        else:
            outputs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'outputs'))
            os.makedirs(outputs_dir, exist_ok=True)

            destination = os.path.join(outputs_dir, filename)
            shutil.move(filename, destination)
            print(f"File saved locally in: {destination}")
        #else:
        #    current_dir = os.getcwd()
        #    new_file_path = os.path.join(current_dir, filename)
        #    os.rename(filename, new_file_path)
        #    print(f"File saved locally at: {new_file_path}")