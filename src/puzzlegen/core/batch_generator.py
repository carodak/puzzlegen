import datetime
import logging
import csv
import os
import shutil
import base64
import sys
from pathlib import Path
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from puzzlegen.core.bfs_solver import BFSSolver
from puzzlegen.core.grid_initializer import GridInitializer
from puzzlegen.core.puzzle_logic import PuzzleLogic
from tqdm import tqdm
from .utils import print_framed
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)

class PuzzleBatchGenerator:
    """
    Generate and manage batches of puzzles by iterating over ranges of parameters.

    This class systematically generates puzzles for each integer value within the given
    ranges of block counts and color counts. For each combination, it attempts to generate
    puzzles solvable within the specified move limit.

    It provides functionality to:
      - Filter out puzzles unsolvable within the move constraints.
      - Collect statistics about solvable and unsolvable puzzles across the batch.
      - Export puzzles visually as PDFs and metadata as CSV files.
      - Display summary charts (bar and pie) to analyze batch characteristics.

    Args:

        blocks_range (tuple[int, int]): Inclusive range of block counts to iterate through (min_blocks, max_blocks).

        colors_range (tuple[int, int]): Inclusive range of color counts to iterate through (min_colors, max_colors).

        colors_blocks (list[str]): List of available colors for blocks.

        nb_moves (int): Maximum number of moves allowed for the optimal solution.

        batch_grid_size (tuple[int, int]): Grid size for each puzzle as (rows, columns).

        batch_stack_probability (float): Probability to stack blocks vertically during puzzle generation.

        blocks_gap (int, optional): Maximum allowed gap between blocks during generation (e.g., 1 means at most one empty cell). Default is 1.


    Attributes:

        puzzle_batch (dict[int, list]): Dictionary mapping move counts to lists of generated puzzles.

        nb_solvables (int): Number of puzzles solvable within the move limit.

        nb_unsolvables (int): Number of puzzles not solvable within the move limit.

        stats (dict[str, int]):  
            Counts of puzzles solvable in 1 up to `nb_moves` moves.  
            Keys are of the form 'solvable_in_X_moves' mapping to counts.  
            Example: {'solvable_in_1_moves': 3, 'solvable_in_2_moves': 4, ...}
            
        csv_data (dict): Data formatted for CSV export.
    """

    def __init__(self, blocks_range, colors_range, colors_blocks, nb_moves, batch_grid_size, nb_attempts=5, batch_stack_probability=0.75, blocks_gap=1):
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
        self.nb_attempts = nb_attempts
        self.batch_stack_probability = batch_stack_probability
        self.blocks_gap = blocks_gap

    def generate_puzzles(self):
        """
        Generate puzzles for all combinations of block and color counts within the specified ranges.

        For each combination:
        - Attempts up to `nb_attempts` times to create a puzzle solvable within `nb_moves`.
        - Stores solvable puzzles grouped by the number of moves required to solve.
        - Updates statistics and prepares data for CSV export.

        Returns:
            dict: Dictionary of generated puzzles grouped by move counts, 
                keys formatted as 'solvable_in_X_moves'.
        """

        print_framed([
            "Generating a batch of puzzles with the following parameters:",
            f"- Block count range: {self.blocks_range}",
            f"- Color count range: {self.colors_range}",
            f"- Color palette: {self.colors}",
            f"- Max number of moves: {self.nb_moves}",
            f"- Grid size: {self.batch_grid_size}",
            f"- Stack probability: {self.batch_stack_probability}"
        ])

        iterated_colors = []
        puzzle_batch = {}
        csv_data = {
            "cubes": [],
            "positions": [],
            "colors": [],
            "moves": []
        }
        stack_probability = self.batch_stack_probability
        blocks_gap = self.blocks_gap

        total_combinations = 0
        for nb_colors in range(self.colors_range[0], self.colors_range[1] + 1):
            iterated_colors = self.colors[:nb_colors]
            for nb_blocks in range(self.blocks_range[0], self.blocks_range[1] + 1):
                if len(iterated_colors) * 3 > nb_blocks:
                    continue
                total_combinations += 1

        for i in range(1, self.nb_moves+1):
            key = 'solvable_in_' + str(i) + '_moves'
            puzzle_batch[key] = []

        with tqdm(total=total_combinations, desc="🧩 Puzzle Batch Generation – Overall Progress") as pbar:
            for nb_colors in range(self.colors_range[0], self.colors_range[1] + 1):
                iterated_colors = self.colors[:nb_colors]
                for nb_blocks in range(self.blocks_range[0], self.blocks_range[1]+1):
                    if len(iterated_colors)*3 > nb_blocks:
                        continue
                    else:
                        if nb_colors == 1:
                            grid_size = (nb_blocks+1, nb_blocks+1)
                        else:
                            grid_size = self.batch_grid_size
                        is_solvable = False
                        logger.info(f"Generating puzzle for {nb_blocks} blocks, colors: {iterated_colors}, grid size: {grid_size}")
                        nb_attempts_ = 0
                        while not(is_solvable) and nb_attempts_ < self.nb_attempts:
                            grid = GridInitializer(grid_size, nb_blocks, iterated_colors, self.nb_moves, stack_probability, blocks_gap)
                            grid.initialize_grid()
                            solver = BFSSolver(grid, PuzzleLogic())
                            is_solvable, solution = solver.perform_all_blocks_moves(display_progress=False)
                            nb_attempts_ = nb_attempts_ + 1
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
                    pbar.update(1)

        self.puzzle_batch = puzzle_batch
        self.csv_data = csv_data
        print("Batch generation completed.")
        return self.puzzle_batch



    def print_and_save_batch(self, filename=None):
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
            BFSSolver.print_history(solved_puzzle, grid_size, False)
        self.print_charts(False)
        if filename is None:
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
        print("🖼️  Close the figure window to continue...")
        plt.show()

    def compute_stats(self):
        """
        Compute and update statistics for the generated puzzle batch.

        Populates the `stats` attribute with counts of puzzles solvable in each number of moves.
        """
        for move in sorted(self.puzzle_batch.keys()):
          self.stats[move] = len(self.puzzle_batch[move])
        print("stats: ", self.stats)

    def set_batch(self, batch):
        """
        Set the current batch of puzzles manually.

        Args:
            batch (dict): Dictionary of puzzles grouped by move count.
        """
        self.puzzle_batch = batch

    def print_charts(self, show):
        """
        Display bar and pie charts summarizing the batch statistics.

        Args:
            show (bool): If True, display the charts.
        """
        labels = list(self.stats.keys()) + ['unsolvable']
        sizes = list(self.stats.values()) + [self.nb_unsolvables]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        x = range(len(labels))
        ax1.bar(x, sizes)
        ax1.set_title('Number of Puzzles Generated (Bar Chart)', pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(labels, rotation=45, ha='right')
        ax1.tick_params(axis='x', labelsize=8)

        wedges, texts, autotexts = ax2.pie(
            sizes,
            labels=None,
            autopct=lambda p: '{:.2f}%({:.0f})'.format(p, (p/100)*sum(sizes)),
            startangle=90,
            wedgeprops=dict(edgecolor='w')
        )
        ax2.set_title('Number of Puzzles Generated (Pie Chart)', pad=20)
        ax2.axis('equal')

        for i, autotext in enumerate(autotexts):
            if autotext.get_text().startswith("0.00%"):
                x, y = autotext.get_position()
                autotext.set_position((x * 1.3, y * 1.3))

        ax2.legend(wedges, labels, title="Legend", loc="center left", bbox_to_anchor=(1, 0.5), fontsize=9)

        fig.tight_layout()

        if show:
            print("🖼️  Close the figure window to continue...")
            plt.show()

    def save_results_as_csv(self, filename=None):
        """
        Save the batch data as a CSV file.

        The CSV contains, for each puzzle:
          - Number of blocks
          - Colors used
          - Initial block positions
          - Number of moves to solve

        Args:
            filename (str, optional): CSV filename. Defaults to a timestamped filename.
        """
        if filename is None:
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
        Save or provide a download link for the file depending on the execution environment.

        Supports:
        - Google Colab: triggers browser download.
        - Jupyter Notebook/Lab: shows a clickable download link.
        - Script or other environments: saves file in 'outputs' directory.

        Args:
            filename (str): Name of the file to save or offer for download.
        """
        try:
            ipython_shell = get_ipython().__class__.__name__
        except NameError:
            ipython_shell = None
        if 'google.colab' in sys.modules:
            from google.colab import files
            files.download(filename)
            print(f"File downloaded in browser (Colab): {filename}")
        elif ipython_shell in ['ZMQInteractiveShell']:
            from IPython.display import display, HTML
            with open(filename, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            download_link = f'<a download="{os.path.basename(filename)}" href="data:application/octet-stream;base64,{b64}" target="_blank">Click here to download {filename}</a>'
            display(HTML(download_link))
            print("File ready for browser download (Jupyter).")
        else:
            outputs_dir = Path(__file__).parent.parent.parent.parent / "outputs"
            outputs_dir.mkdir(parents=True, exist_ok=True)
            destination = outputs_dir / Path(filename).name
            shutil.move(filename, destination)
            print(f"File saved locally at: {destination}")