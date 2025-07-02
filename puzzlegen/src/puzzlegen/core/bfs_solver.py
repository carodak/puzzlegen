#######
import logging
from collections import deque
from matplotlib import pyplot as plt
from matplotlib.patches import FancyArrowPatch

logging.getLogger().setLevel(logging.INFO)

class BFSSolver:
    """
    A solver that uses Breadth-First Search (BFS) to explore possible move sequences 
    and determine whether a puzzle configuration can be solved.

    This class delegates puzzle-specific logic (gravity, move execution, match detection) 
    to external components provided via `grid_initializer` and `puzzle_logic`.
    """
    def __init__(self, grid_initializer, puzzle_logic):
        """
        Initialize the BFSSolver with a grid and puzzle logic instance.

        Args:
            grid_initializer (GridInitializer): Handles initial puzzle setup and parameters.
            puzzle_logic (PuzzleLogic): Provides core puzzle mechanics (moves, gravity, match detection).
        """
        self.grid_initializer = grid_initializer
        self.puzzle_logic = puzzle_logic

    def perform_all_blocks_moves(self):
        """
        Attempt to solve the puzzle using Breadth-First Search (BFS) within a limited number of moves.

        This function explores all possible sequences of valid block moves (simple or exchange)
        using a BFS strategy to determine whether the current puzzle configuration can be solved
        in `min_nb_moves` steps or fewer.

        It starts from the initial grid state and simulates possible actions at each round. Each node 
        in the search tree tracks the history of block positions, moves performed, and puzzle states.
        The exploration stops when either a solution is found or the search depth exceeds the allowed limit.

        Returns:
            tuple:
                - is_solvable (bool): True if a valid solution is found within the move limit, False otherwise.
                - solution (dict): A dictionary containing the move history and block states leading to the solution,
                                or an empty dict if no solution was found.
        """
        min_moves_to_solve = self.grid_initializer.min_nb_moves
        initial_set_blocks = self.grid_initializer.set_blocks.copy()
        grid_size = self.grid_initializer.grid_size
        colors = self.grid_initializer.colors

        queue = deque()
        current_round = 0
        initial_node = {
            "set_blocks_history": [initial_set_blocks],
            "moves_types_history": [],
            "moved_blocks_history" : [],
            "rounds_number_history": [1],
            "puzzle_states_history" : [1]
        }
        queue.append(initial_node)

        #print(f"\n\n..::SOLVER STEP:.. Checking if the puzzle has a solution in {min_moves_to_solve} moves\n")
        while queue:
          current_item = queue.popleft()

          set_blocks = current_item["set_blocks_history"][-1].copy()
          current_round = current_item["rounds_number_history"][-1]
          if current_round > min_moves_to_solve:
            break
          puzzle_state = current_item["puzzle_states_history"][-1]

          #logging.debug(f"\n\nWe are simulating round: {current_round} and the following set of blocks: {set_blocks} \n")

          if puzzle_state == 1:
            is_solvable, solution = self.process_possible_moves(set_blocks, current_item, current_round, grid_size, colors, queue)
            if is_solvable:
              return True, solution
        print(f"Did not find a solution in {current_round-1} moves. See the queue")
        return False, {}

    def process_possible_moves(self, set_blocks, current_item, current_round, grid_size, colors, queue):
        """
        Explore and enqueue all valid moves from the current puzzle state in the BFS process.

        For each block in the current grid state, this method checks all possible move types 
        (simple moves and exchanges to the left and right). For each valid move:
        - The move is applied to a copy of the current block set.
        - Gravity and match elimination are applied to the updated grid.
        - The new state is evaluated and stored in a new BFS node.
        - This new node is appended to the BFS queue for further exploration.

        If a terminal game state is reached (e.g., state == 3), a solution is extracted and returned immediately.

        Args:
            set_blocks (dict): Dictionary of current block positions and Block objects.
            current_item (dict): Current BFS node containing history of previous states and moves.
            current_round (int): The current depth (round) in the BFS search tree.
            grid_size (tuple): Tuple indicating grid dimensions (rows, columns).
            colors (list): List of allowed block colors.
            queue (deque): The BFS queue, to which new valid states will be appended.

        Returns:
            tuple:
                - is_solvable (bool): True if a solution is found in this branch, False otherwise.
                - solution (dict): Dictionary containing the history of moves and states leading to the solution,
                                or an empty dict if no solution is found at this level.
        """
        for position, block in set_blocks.items():
          possible_moves = self.puzzle_logic.check_all_available_moves(position, block.color, set_blocks, grid_size)
          for move_type in ['move_left', 'move_right', 'exchange_left', 'exchange_right']:
            updated_blocks = set_blocks.copy()
            if possible_moves[move_type]:
              updated_blocks = self.puzzle_logic.make_move(move_type, position, updated_blocks)
              updated_blocks = self.puzzle_logic.apply_gravity_and_eliminate_matches(updated_blocks, grid_size)
              state = self.puzzle_logic.get_game_state(updated_blocks, colors)

              next_node = {
                        "set_blocks_history": current_item["set_blocks_history"] + [updated_blocks],
                        "moves_types_history": current_item["moves_types_history"] + [move_type],
                        "moved_blocks_history" : current_item["moved_blocks_history"] + [position],
                        "rounds_number_history": current_item["rounds_number_history"] + [current_round+1],
                        "puzzle_states_history" : current_item["puzzle_states_history"] + [state]
              }
              queue.append(next_node)
              if state == 3:
                solution = self.process_solution(next_node, current_round)
                return True, solution
        return False, {}

    def process_solution(self, solved_puzzle_dict, current_round):
        """
        Finalize and return the solution after the puzzle is solved.

        This function adds empty entries to the move history to mark the end,
        prints the solution path, and returns it.

        Args:
            solved_puzzle_dict (dict): Contains the steps that led to the solution.
            current_round (int): Number of moves it took to solve the puzzle.

        Returns:
            dict: The completed solution dictionary.
        """
        solved_puzzle_dict["moves_types_history"].append('')
        solved_puzzle_dict["moved_blocks_history"].append(())

        print(f"Found a solution: {solved_puzzle_dict['set_blocks_history']} in {current_round} moves \n")
        return solved_puzzle_dict

    @staticmethod
    def print_history(solved_puzzle_dict, grid_size, show, ax=None):
        """
        Visualize the full sequence of moves that solved the puzzle.

        This function creates a series of side-by-side grid plots, one for each step
        in the solution. It highlights moved blocks and shows arrows indicating moves.
        The initial and final grid states are labeled clearly.

        Args:
            solved_puzzle_dict (dict): Dictionary containing the history of grid states,
                                    moves, and block positions from the solver.
            grid_size (tuple): Size of the puzzle grid (rows, columns).
            show (bool): If True, the plot is displayed using matplotlib.
            ax (matplotlib.axes.Axes, optional): Optional axis to plot on (useful for embedding).

        Returns:
            None
        """
        set_blocks_history = solved_puzzle_dict["set_blocks_history"]
        moved_blocks_history = solved_puzzle_dict["moved_blocks_history"]
        moves_types_history = solved_puzzle_dict["moves_types_history"]
        rounds_number_history = solved_puzzle_dict["rounds_number_history"]

        if ax is None:
            num_subplots = len(set_blocks_history)
            fig, ax = plt.subplots(1, num_subplots, figsize=(num_subplots * 6, 8), sharey=True, **{"squeeze": False})
            #plt.subplots_adjust(bottom=0.1, top=0.9, left=0.05, right=0.95)

        for i in range(len(set_blocks_history)):
            set_blocks = set_blocks_history[i]
            move_type = moves_types_history[i]
            position = moved_blocks_history[i]
            round = rounds_number_history[i]
            title = ""

            grid = [['white' for _ in range(grid_size[1])] for _ in range(grid_size[0])]
            for pos, block in set_blocks.items():
                row, col = pos
                grid[row][col] = block.color

            for row in range(grid_size[0]):
                for col in range(grid_size[1]):
                    color = grid[row][col]
                    rect = plt.Rectangle((col, grid_size[0] - row - 1), 1, 1, facecolor=color, edgecolor='black')
                    ax[0, i].add_patch(rect)

            if i == 0:
                title = f"..::SOLUTION::..: Solvable in {rounds_number_history[-2]} moves (blocks positions: {set_blocks})\n\nINITIAL STATE: "

            if i != len(set_blocks_history) - 1:
                title += f"(MOVE {round}) \nPerform: {move_type} at position: {position}:"
                ax[0, i], grid = BFSSolver.highlight_moved_block(set_blocks, position, ax[0, i], grid, grid_size)
                ax[0, i], grid = BFSSolver.draw_arrow(set_blocks, position, move_type, ax[0, i], grid, grid_size)
            else:
                title = "FINAL STATE"

            ax[0, i].set_aspect('equal')
            ax[0, i].axis('off')
            ax[0, i].set_xlim(-0.5, grid_size[1] + 0.5)
            ax[0, i].set_ylim(-0.5, grid_size[0] + 0.5)
            ax[0, i].set_title(title, loc='left')

        if show:
            plt.tight_layout()
            plt.show()

    @staticmethod
    def highlight_moved_block(set_blocks, position, ax, grid, grid_size):
        """
        Visually highlight the block that was moved by drawing a lime-colored border around it.

        Args:
            set_blocks (dict): Dictionary of current block positions and their colors.
            position (tuple): (row, col) coordinates of the moved block.
            ax (matplotlib.axes.Axes): The matplotlib axis on which to draw.
            grid (list): 2D list representing the grid colors.
            grid_size (tuple): Size of the grid (rows, columns).

        Returns:
            tuple: (ax, grid) — The updated axis and grid, unchanged except for visualization.
        """
        arrow_pos_row = position[0]
        arrow_pos_col = position[1]
        color = grid[arrow_pos_row][arrow_pos_col]
        rect = plt.Rectangle((arrow_pos_col, grid_size[0] - arrow_pos_row - 1), 1, 1, facecolor=color, edgecolor='lime', linewidth=2)
        ax.add_patch(rect)
        return ax, grid

    @staticmethod
    def draw_arrow(set_blocks, position, move_type, ax, grid, grid_size):
        """
        Draw an arrow on the plot to indicate the direction of a block’s move.

        Args:
            set_blocks (dict): Dictionary of current block positions and their colors.
            position (tuple): (row, col) coordinates of the moved block.
            move_type (str): Type of move performed (e.g., 'move_left', 'exchange_right').
            ax (matplotlib.axes.Axes): The matplotlib axis on which to draw the arrow.
            grid (list): 2D list representing the grid colors.
            grid_size (tuple): Size of the grid (rows, columns).

        Returns:
            tuple: (ax, grid) — The updated axis and grid, with the arrow added for visualization.
        """
        arrow_pos_row = position[0]
        arrow_pos_col = position[1]
        linecol = "lime"
        arrow = BFSSolver.create_fancy_arrow_patch(arrow_pos_col, arrow_pos_row, move_type, linecol, grid_size)
        ax.add_patch(arrow)
        return ax, grid

    @staticmethod
    def create_fancy_arrow_patch(arrow_pos_col, arrow_pos_row, move_type, linecol, grid_size):
        """
        Create a FancyArrowPatch for move visualization.

        Args:
            arrow_pos_col (int): Column of the arrow start.
            arrow_pos_row (int): Row of the arrow start.
            move_type (str): Type of move.
            linecol (str): Color of the arrow.
            grid_size (tuple): Size of the grid.

        Returns:
            FancyArrowPatch: The arrow patch object.
        """
        if move_type == "move_left":
            arrow_start = (arrow_pos_col - 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow_end = (arrow_pos_col + 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='<-', mutation_scale=30, linewidth=2, color=linecol)
        elif move_type == "move_right":
            arrow_start = (arrow_pos_col + 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow_end = (arrow_pos_col + 1.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='->', mutation_scale=30, linewidth=2, color=linecol)
        elif move_type == "exchange_left":
            arrow_start = (arrow_pos_col - 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow_end = (arrow_pos_col + 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='<->', mutation_scale=30, linewidth=2, color=linecol)
        elif move_type == "exchange_right":
            arrow_start = (arrow_pos_col + 0.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow_end = (arrow_pos_col + 1.5, grid_size[0] - arrow_pos_row - 0.5)
            arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='<->', mutation_scale=30, linewidth=2, color=linecol)
        return arrow

