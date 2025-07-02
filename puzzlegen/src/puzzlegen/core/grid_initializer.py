import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import random
from matplotlib.patches import Rectangle
from matplotlib import colors

from .utils import assign_blocks_per_color, sort_blocks_by_rows
from .block import Block

mpl.rcParams['figure.max_open_warning'] = 50  # Increase the maximum number of warnings

class GridInitializer:
    """GridInitializer Class: This class is responsible for handling the setup of the game board, including generating the initial configuration of blocks.
    """
    def __init__(self, grid_size, nb_blocks, colors, min_nb_moves, stack_probability, blocks_gap):
        """
        Initialize the GridInitializer.

        Args:
            grid_size (tuple): Size of the grid as (rows, columns).
            nb_blocks (int): Number of blocks to place.
            colors (list): List of block colors.
            min_nb_moves (int): Minimum number of moves to solve.
            stack_probability (float): Probability of stacking blocks.
            blocks_gap (int): Minimum gap between blocks in the same row.
        """
        self.grid_size = grid_size
        self.nb_blocks = nb_blocks
        self.colors = colors
        self.set_blocks = {}
        self.min_nb_moves = min_nb_moves
        self.stack_probability = stack_probability
        self.blocks_gap = blocks_gap

    def is_valid_position(self, row, col):
        """
        Check if a position is within the grid bounds.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if position is valid, False otherwise.
        """
        if row < 0 or row >= self.grid_size[0] or col < 0 or col >= self.grid_size[1]:
            return False
        return True

    def is_block_present(self, row, col):
        """
        Check if a block is present at the given position.

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            list: [True, color] if block is present, [False, None] otherwise.
        """
        if self.is_valid_position(row, col):
            if (row, col) in self.set_blocks:
                block = self.set_blocks[(row, col)]
                block_color = block.color
            else:
                block_color = None
            return [block_color is not None, block_color]
        return [False, None]

    def is_similar_block(self, row, col, color):
        """
        Check if a block of the same color is present at the given position.

        Args:
            row (int): Row index.
            col (int): Column index.
            color (str): Color to check.

        Returns:
            bool: True if a similar block is present, False otherwise.
        """
        block_present = self.is_block_present(row, col)
        if self.is_valid_position(row, col) and block_present[0] and block_present[1] == color:
            return True

    def check_valid_placement(self, row, col, color):
        """
        Check if placing a block at the given position is valid according to the rules (no matches are allowed during initial setup).

        Args:
            row (int): Row index.
            col (int): Column index.
            color (str): Color of the block.

        Returns:
            bool: True if placement is valid, False otherwise.
        """
        if self.is_similar_block(row + 1, col, color) and self.is_similar_block(row + 2, col, color):
            return False
        if self.is_similar_block(row, col-1, color) and self.is_similar_block(row, col+1, color):
            return False
        if self.is_similar_block(row, col-1, color) and self.is_similar_block(row, col-2, color):
            return False
        if self.is_similar_block(row, col+1, color) and self.is_similar_block(row, col+2, color):
            return False
        return True

    def get_highest_positions(self):
        """
        Get the highest (topmost) block positions for each column.

        Returns:
            list: List of (row, col) tuples representing the highest block in each column.
        """
        highest_positions = {}
        for position in self.set_blocks:
            row, col = position
            if col not in highest_positions or row < highest_positions[col][0]:
                highest_positions[col] = (row, col)
        highest_block_positions = list(highest_positions.values())
        return highest_block_positions

    def select_random_highest_position(self):
        """
        Select a random position above the highest block in a random column or return an empty position with a gap.

        Returns:
            tuple: (row, col) position above a random highest block, or an empty position with gap if none found.
        """
        highest_block_positions = self.get_highest_positions()
        highest_block_positions_filtered = [(row, col) for row, col in highest_block_positions if row != 0]
        if not highest_block_positions_filtered:
            return self.select_empty_positions_with_gap()
        random_position = random.choice(highest_block_positions_filtered)
        return (random_position[0]-1,random_position[1])

    def get_empty_positions_with_gap(self):
        """
        Get empty positions in the bottomost row that respect the minimum gap between blocks.

        Returns:
            list: List of (row, col) tuples for valid empty positions.
        """
        last_row = self.grid_size[0] - 1
        empty_positions_with_gap = []
        highest_positions = self.get_highest_positions()

        for row, col in highest_positions:
            adjacent_cols = [col + self.blocks_gap, col + self.blocks_gap + 1, col - self.blocks_gap, col - self.blocks_gap - 1]
            adjacent_cols = [adj_col for adj_col in adjacent_cols if adj_col >= 0 and adj_col < self.grid_size[1]]

            for adj_col in adjacent_cols:
                adjacent_position = (last_row, adj_col)
                if adjacent_position not in self.set_blocks:
                    empty_positions_with_gap.append(adjacent_position)

        return empty_positions_with_gap

    def select_empty_positions_with_gap(self):
        """
        Select a random empty position in the last row that respects the minimum gap.

        Returns:
            tuple: (row, col) position.
        """
        empty_positions_with_gap = self.get_empty_positions_with_gap()
        if not empty_positions_with_gap:
            return self.select_random_highest_position()
        random_position = random.choice(empty_positions_with_gap)
        return random_position

    def initialize_grid(self):
        """
        Initialize the grid with blocks according to the rules and constraints.
        
        The method performs the following steps:
          - Determines the number of blocks to place per color using `assign_blocks_per_color`.
          - Creates a list of blocks to place, respecting the color distribution.
          - Iteratively places each block in the grid, either stacking on existing blocks or
            placing in empty positions that respect minimum spacing (gap) constraints.
          - The first block is placed near the center top of the grid.
          - For subsequent blocks, the placement is either stacked on top of existing blocks (with a
            probability defined by `stack_probability`) or placed in valid empty positions.
          - Each potential placement is validated by `check_valid_placement` to avoid rule violations (e.g., no immediate matches).
          - Once placed, blocks are recorded in `self.set_blocks` with their positions as keys.
          - Finally, `self.set_blocks` is sorted by row to maintain a consistent order.

        This process ensures the initial puzzle grid respects the game's placement rules
        and sets up a valid starting configuration for the puzzle.

        Returns:
            None
        """
        blocks_per_color = assign_blocks_per_color(self.nb_blocks, self.colors)
        blocks_to_place = [color for color, count in blocks_per_color for i in range(count)]
        while blocks_to_place:
            placed = False
            while not(placed):
                stacked = False
                if random.random() < self.stack_probability:
                    stacked = True
                random_block_index = random.randrange(len(blocks_to_place))
                random_block_color = blocks_to_place[random_block_index]
                if not self.set_blocks:
                    random_column_grid = math.floor(self.grid_size[1]/2)
                    selected_row = self.grid_size[0]-1
                elif not stacked:
                    random_position = self.select_empty_positions_with_gap()
                    random_column_grid = random_position[1]
                    selected_row = random_position[0]
                if stacked and self.set_blocks:
                    random_position = self.select_random_highest_position()
                    random_column_grid = random_position[1]
                    selected_row = random_position[0]

                if self.check_valid_placement(selected_row, random_column_grid, random_block_color):
                    block = Block(random_block_color)
                    self.set_blocks[(selected_row, random_column_grid)] = block
                    placed = True
            blocks_to_place.pop(random_block_index)
        self.set_blocks = sort_blocks_by_rows(self.set_blocks)

    def change_set_blocks(self, set_blocks):
        """
        Change the current set of blocks to a new configuration.

        Args:
            set_blocks (dict): New set of blocks.
        """
        self.set_blocks = set_blocks

    @staticmethod
    def init_graphical_grid(set_blocks, grid_size):
        """
        Create a graphical representation of the puzzle grid using matplotlib.

        This method builds a 2D color grid from the set of placed blocks, then draws it using 
        matplotlib by rendering each cell as a colored rectangle. The Y-axis is flipped so that 
        row 0 appears at the bottom, consistent with a bottom-up grid orientation.

        Args:
            set_blocks (dict): Dictionary mapping (row, col) positions to Block objects. Each block
                                contains a `color` attribute used for rendering.
            grid_size (tuple): A (rows, columns) tuple indicating the dimensions of the grid.

        Returns:
            tuple: (fig, ax, grid)
                - fig (matplotlib.figure.Figure): The matplotlib figure object.
                - ax (matplotlib.axes.Axes): The matplotlib axis with rendered grid.
                - grid (list of lists): 2D list of cell colors representing the grid state.
        """
        grid = [['white' for _ in range(grid_size[1])] for _ in range(grid_size[0])]
        for position, block in set_blocks.items():
            row, col = position
            grid[row][col] = block.color

        fig, ax = plt.subplots()
        ax.axis('off')
        for row in range(grid_size[0]):
            for col in range(grid_size[1]):
                color = grid[row][col]
                rect = plt.Rectangle((col, grid_size[0] - row - 1), 1, 1, facecolor=color, edgecolor='black')
                ax.add_patch(rect)

        return fig, ax, grid

    def print_initial_grid(self):
        """
        Print and display the initial grid using matplotlib.
        """
        fig, ax, grid = GridInitializer.init_graphical_grid(self.set_blocks, self.grid_size)
        ax.set_aspect('equal')
        ax.set_xlim(-0.5, self.grid_size[1] + 0.5)
        ax.set_ylim(-0.5, self.grid_size[0] + 0.5)
        print("Here is the randomly-created Puzzle: ")
        plt.show()
        print("\nOr a shorter representation: \n", self.set_blocks)
