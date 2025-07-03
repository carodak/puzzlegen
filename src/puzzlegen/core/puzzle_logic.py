from collections import Counter, deque
from .utils import sort_blocks_by_rows, sort_blocks_by_columns
class PuzzleLogic():
    """
    PuzzleLogic Class: Contains methods responsible for the game's core logic.
    This includes checking for block elimination, enforcing gravity rules (making blocks fall down after elimination),
    and performing player moves (e.g., swapping two adjacent blocks).
    """
    def __init__(self):
        """Initialize the PuzzleLogic class."""
        return

    def check_all_available_moves(self, current_position, color, set_blocks, grid_size):
        """
        Check all possible moves for a block at the given position.

        Args:
            current_position (tuple): (row, col) position of the block.
            color (str): Color of the block.
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            dict: Dictionary with possible moves as keys and booleans as values.
        """
        possible_moves = {
            'move_left': self.can_move_left(current_position, set_blocks),
            'move_right': self.can_move_right(current_position, set_blocks, grid_size),
            'exchange_left': self.can_exchange_left(current_position, color, set_blocks),
            'exchange_right': self.can_exchange_right(current_position, color, set_blocks, grid_size)
        }
        return possible_moves

    def can_move_left(self, position, set_blocks):
        """
        Check if a block can move left to an unoccupied space.

        Args:
            position (tuple): (row, col) position of the block.
            set_blocks (dict): Current set of blocks.

        Returns:
            bool: True if the block can move left, False otherwise.
        """
        row, col = position
        if col > 0:
            left_position = (row, col - 1)
            return left_position not in set_blocks
        return False

    def can_move_right(self, position, set_blocks, grid_size):
        """
        Check if a block can move right to an unoccupied space.

        Args:
            position (tuple): (row, col) position of the block.
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            bool: True if the block can move right, False otherwise.
        """
        row, col = position
        if col < grid_size[1] - 1:
            right_position = (row, col + 1)
            return right_position not in set_blocks
        return False

    def can_exchange_left(self, position, color, set_blocks):
        """
        Check if a block can exchange with the block to its left.

        Args:
            position (tuple): (row, col) position of the block.
            color (str): Color of the block.
            set_blocks (dict): Current set of blocks.

        Returns:
            bool: True if the block can exchange left, False otherwise.
        """
        row, col = position
        if col > 0:
            left_position = (row, col - 1)
            return left_position in set_blocks and color != set_blocks[left_position].color
        return False

    def can_exchange_right(self, position, color, set_blocks, grid_size):
        """
        Check if a block can exchange with the block to its right.

        Args:
            position (tuple): (row, col) position of the block.
            color (str): Color of the block.
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            bool: True if the block can exchange right, False otherwise.
        """
        row, col = position
        if col < grid_size[1] - 1:
            right_position = (row, col + 1)
            return right_position in set_blocks and color != set_blocks[right_position].color
        return False

    def update_block(self, old_position, new_position, set_blocks):
        """
        Update the position of a block in the set_blocks dictionary.

        Args:
            old_position (tuple): Previous (row, col) position.
            new_position (tuple): New (row, col) position.
            set_blocks (dict): Current set of blocks.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        saved_block = set_blocks.pop(old_position)
        set_blocks[new_position] = saved_block
        set_blocks = sort_blocks_by_rows(set_blocks)
        return set_blocks

    def exchange_block(self, first_position, second_position, set_blocks):
        """
        Exchange two blocks in the set_blocks dictionary.

        Args:
            first_position (tuple): (row, col) of the first block.
            second_position (tuple): (row, col) of the second block.
            set_blocks (dict): Current set of blocks.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        block_1 = set_blocks[first_position]
        block_2 = set_blocks[second_position]
        set_blocks[first_position] = block_2
        set_blocks[second_position] = block_1
        set_blocks = sort_blocks_by_rows(set_blocks)
        return set_blocks

    def has_matches(self, set_blocks):
        """
        Check if there are any matches (3 or more aligned blocks of the same color).

        Args:
            set_blocks (dict): Current set of blocks.

        Returns:
            bool: True if matches exist, False otherwise.
        """
        return bool(self.find_matches(set_blocks))

    def find_matches(self, set_blocks):
        """
        Find all matches (3 or more aligned blocks of the same color).

        Args:
            set_blocks (dict): Current set of blocks.

        Returns:
            set: Set of positions where matches are found.
        """
        matches = set()

        matches |= self.find_matches_by_rows(set_blocks)
        matches |= self.find_matches_by_columns(set_blocks)

        return matches

    def find_matches_by_rows(self, set_blocks):
        """
        Find all horizontal matches in the set_blocks.

        Args:
            set_blocks (dict): Current set of blocks.

        Returns:
            set: Set of positions where horizontal matches are found.
        """
        matches = set()

        set_blocks_row = sort_blocks_by_rows(set_blocks)
        matches |= self.find_matches_in_iterator(set_blocks_row.items(), is_same_row=True)

        return matches

    def find_matches_by_columns(self, set_blocks):
        """
        Find all vertical matches in the set_blocks.

        Args:
            set_blocks (dict): Current set of blocks.

        Returns:
            set: Set of positions where vertical matches are found.
        """
        matches = set()

        set_blocks_column = sort_blocks_by_columns(set_blocks)
        matches |= self.find_matches_in_iterator(set_blocks_column.items(), is_same_row=False)

        return matches

    def find_matches_in_iterator(self, set_blocks, is_same_row):
        """
        Helper function to find matches in an iterator (row or column).

        Args:
            set_blocks (iterator): Iterator over set_blocks items.
            is_same_row (bool): True for row, False for column.

        Returns:
            set: Set of positions where matches are found.
        """
        matches = set()
        tmp_matches = set()
        nb_aligned = 1

        try:
            iterator = iter(set_blocks)
            (position, block) = next(iterator)
            while True:
                (next_position, next_block) = next(iterator)
                if self.is_aligned(position, next_position, block, next_block, is_same_row):
                    nb_aligned += 1
                    tmp_matches.add(position)
                    tmp_matches.add(next_position)
                else:
                    nb_aligned = 1
                    tmp_matches = set()

                if nb_aligned >= 3:
                    matches |= tmp_matches

                position, block = next_position, next_block

        except StopIteration:
            pass

        return matches

    def delete_matches(self, set_blocks, matches):
        """
        Delete all matched blocks from the set_blocks.

        Args:
            set_blocks (dict): Current set of blocks.
            matches (set): Set of positions to delete.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        new_set_blocks = set_blocks.copy()
        for key in matches:
            if key in new_set_blocks:
                del new_set_blocks[key]
        return new_set_blocks

    def is_aligned(self, position, next_position, block, next_block, is_same_row):
        """
        Check if two blocks are aligned and of the same color.

        Args:
            position (tuple): (row, col) of the first block.
            next_position (tuple): (row, col) of the second block.
            block (Block): First block.
            next_block (Block): Second block.
            is_same_row (bool): True for row, False for column.

        Returns:
            bool: True if aligned and same color, False otherwise.
        """
        if is_same_row:
            return position[0] == next_position[0] and position[1] == next_position[1] - 1 and block.color == next_block.color
        else:
            return position[1] == next_position[1] and position[0] == next_position[0] - 1 and block.color == next_block.color

    def has_gravity(self, set_blocks, grid_size):
        """
        Check if any block can fall due to gravity.

        Args:
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            bool: True if gravity applies, False otherwise.
        """
        return bool(self.apply_gravity(set_blocks, grid_size) != set_blocks)

    def apply_gravity(self, set_blocks, grid_size):
        """
        Apply gravity to all blocks (make unsupported blocks fall).

        For each block in the grid (processed from bottom to top), this function checks whether
        there is empty space directly beneath it. If so, it allows the block to fall vertically 
        until it lands on either another block or the bottom of the grid.

        Args:
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            dict: Updated set_blocks dictionary after gravity.
        """
        new_set_blocks = set_blocks.copy()
        for position in reversed(set_blocks):
            row, col = position
            underneath_position = (row + 1, col)

            while underneath_position[0] < grid_size[0] and underneath_position not in new_set_blocks:
              underneath_position = (underneath_position[0] + 1, underneath_position[1])

            new_position = (underneath_position[0] - 1, underneath_position[1])
            if new_position != position:
              new_set_blocks = self.update_block(position, new_position, new_set_blocks)
        return new_set_blocks

    def apply_gravity_and_eliminate_matches(self, set_blocks, grid_size):
        """
        Apply gravity and eliminate matches repeatedly until stable.

        Args:
            set_blocks (dict): Current set of blocks.
            grid_size (tuple): Size of the grid.

        Returns:
            dict: Updated set_blocks dictionary after gravity and elimination.
        """
        new_set_blocks = set_blocks.copy()
        while True:
            new_set_blocks_before = new_set_blocks.copy()
            new_set_blocks = self.apply_gravity(new_set_blocks, grid_size)
            new_set_blocks = self.delete_matches(new_set_blocks,self.find_matches(new_set_blocks))
            if new_set_blocks == new_set_blocks_before:
                break
        return new_set_blocks

    def make_move(self, move_type, position, set_blocks):
        """
        Perform a move (either a simple shift or an exchange) on a given block in the grid (set_blocks).

        Args:
            move_type (str): Type of move ('move_left', 'move_right', etc.).
            position (tuple): (row, col) of the block to move.
            set_blocks (dict): Current set of blocks.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        if move_type == "move_left":
            set_blocks = self.make_simple_move(position, "left", set_blocks)
        elif move_type == "move_right":
            set_blocks = self.make_simple_move(position, "right", set_blocks)
        elif move_type == "exchange_left":
            set_blocks = self.make_exchange_move(position, "left", set_blocks)
        elif move_type == "exchange_right":
            set_blocks = self.make_exchange_move(position, "right", set_blocks)
        return set_blocks

    def make_simple_move(self, position, direction, set_blocks):
        """
        Perform a simple move (left or right) for a given block.

        Args:
            position (tuple): (row, col) of the block.
            direction (str): 'left' or 'right'.
            set_blocks (dict): Current set of blocks.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        if direction == "left":
          new_position = (position[0], position[1]-1)
          set_blocks = self.update_block(position, new_position, set_blocks)
        elif direction == "right":
          new_position = (position[0], position[1]+1)
          set_blocks = self.update_block(position, new_position, set_blocks)
        return set_blocks

    def make_exchange_move(self, position, direction, set_blocks):
        """
        Perform an exchange move (left or right) for a given block.

        Args:
            position (tuple): (row, col) of the block.
            direction (str): 'left' or 'right'.
            set_blocks (dict): Current set of blocks.

        Returns:
            dict: Updated set_blocks dictionary.
        """
        if direction == "left":
          new_position = (position[0], position[1]-1)
          set_blocks = self.exchange_block(position, new_position, set_blocks)
        elif direction == "right":
          new_position = (position[0], position[1]+1)
          set_blocks = self.exchange_block(position, new_position, set_blocks)
        return set_blocks

    def get_game_state(self, set_blocks, colors):
        """
        Get the current game state.

        Args:
            set_blocks (dict): Current set of blocks.
            colors (list): List of block colors.

        Returns:
            int: 3 for victory, 2 for defeat, 1 for in progress.
        """
        if not set_blocks:
          return 3
        elif not self.has_valid_block_color_counts(set_blocks, colors):
          return 2
        else:
          return 1

    def has_valid_block_color_counts(self, set_blocks, colors):
        """
        Check if all colors have at least 3 blocks.

        Args:
            set_blocks (dict): Current set of blocks.
            colors (list): List of block colors.

        Returns:
            bool: True if valid, False otherwise.
        """
        color_counts = self.count_block_colors(set_blocks)
        for color in colors:
            if color_counts[color] == 1 or color_counts[color] == 2:
                return False
            else:
                return True

    def count_block_colors(self, set_blocks):
        """
        Count the number of blocks for each color.

        Args:
            set_blocks (dict): Current set of blocks.

        Returns:
            Counter: Counter object with color counts.
        """
        color_counts = Counter(block.color for block in set_blocks.values())
        return color_counts
