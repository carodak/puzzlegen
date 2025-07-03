import unittest
from unittest.mock import MagicMock
from puzzlegen.core.bfs_solver import BFSSolver

class TestBFSSolver(unittest.TestCase):
    def setUp(self):
        # Mock GridInitializer and PuzzleLogic
        self.mock_grid_initializer = MagicMock()
        self.mock_puzzle_logic = MagicMock()
        self.mock_grid_initializer.min_nb_moves = 2
        self.mock_grid_initializer.set_blocks = {(0, 0): MagicMock(color='red')}
        self.mock_grid_initializer.grid_size = (3, 3)
        self.mock_grid_initializer.colors = ['red', 'blue']

        self.solver = BFSSolver(self.mock_grid_initializer, self.mock_puzzle_logic)

    def test_perform_all_blocks_moves_no_solution(self):
        # Simulate always returning state != 3 (never solved)
        self.mock_puzzle_logic.check_all_available_moves.return_value = {
            'move_left': False, 'move_right': False, 'exchange_left': False, 'exchange_right': False
        }
        self.mock_puzzle_logic.get_game_state.return_value = 1
        is_solvable, solution = self.solver.perform_all_blocks_moves()
        self.assertFalse(is_solvable)
        self.assertEqual(solution, {})

    def test_process_solution_appends_empty_move(self):
        solved_puzzle_dict = {
            "moves_types_history": ['move_left'],
            "moved_blocks_history": [(0, 0)],
            "set_blocks_history": [{(0, 0): MagicMock(color='red')}]
        }
        result = self.solver.process_solution(solved_puzzle_dict, 1)
        self.assertEqual(result["moves_types_history"][-1], '')
        self.assertEqual(result["moved_blocks_history"][-1], ())

    def test_highlight_moved_block(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        set_blocks = {(0, 0): MagicMock(color='red')}
        grid = [['red']]
        grid_size = (1, 1)
        ax, grid = BFSSolver.highlight_moved_block(set_blocks, (0, 0), ax, grid, grid_size)
        self.assertIsNotNone(ax)

    def test_draw_arrow(self):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        set_blocks = {(0, 0): MagicMock(color='red')}
        grid = [['red']]
        grid_size = (1, 1)
        ax, grid = BFSSolver.draw_arrow(set_blocks, (0, 0), "move_left", ax, grid, grid_size)
        self.assertIsNotNone(ax)

    def test_create_fancy_arrow_patch(self):
        arrow = BFSSolver.create_fancy_arrow_patch(0, 0, "move_left", "lime", (3, 3))
        self.assertIsNotNone(arrow)
        arrow = BFSSolver.create_fancy_arrow_patch(0, 0, "move_right", "lime", (3, 3))
        self.assertIsNotNone(arrow)
        arrow = BFSSolver.create_fancy_arrow_patch(0, 0, "exchange_left", "lime", (3, 3))
        self.assertIsNotNone(arrow)
        arrow = BFSSolver.create_fancy_arrow_patch(0, 0, "exchange_right", "lime", (3, 3))
        self.assertIsNotNone(arrow)

if __name__ == '__main__':
    unittest.main()