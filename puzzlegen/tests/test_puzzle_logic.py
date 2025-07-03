import unittest
from unittest.mock import MagicMock, patch
from puzzlegen.core.puzzle_logic import PuzzleLogic

class TestPuzzleLogic(unittest.TestCase):
    def setUp(self):
        self.logic = PuzzleLogic()
        self.set_blocks = {
            (0, 0): MagicMock(color='red'),
            (0, 1): MagicMock(color='blue'),
            (0, 2): MagicMock(color='red'),
            (1, 0): MagicMock(color='red'),
            (1, 1): MagicMock(color='red'),
            (1, 2): MagicMock(color='red'),
        }
        self.grid_size = (3, 3)
        self.colors = ['red', 'blue']

    def test_check_all_available_moves(self):
        moves = self.logic.check_all_available_moves((0, 1), 'blue', self.set_blocks, self.grid_size)
        self.assertIsInstance(moves, dict)
        self.assertIn('move_left', moves)
        self.assertIn('move_right', moves)
        self.assertIn('exchange_left', moves)
        self.assertIn('exchange_right', moves)

    def test_can_move_left_and_right(self):
        # Block at (0, 1) can move left (since (0, 0) is occupied, should be False)
        self.assertFalse(self.logic.can_move_left((0, 1), self.set_blocks))
        # Block at (0, 2) can move right (out of bounds, should be False)
        self.assertFalse(self.logic.can_move_right((0, 2), self.set_blocks, self.grid_size))
        # Block at (0, 1) can move right (since (0, 2) is occupied, should be False)
        self.assertFalse(self.logic.can_move_right((0, 1), self.set_blocks, self.grid_size))

    def test_can_exchange_left_and_right(self):
        # Block at (0, 1) can exchange left with (0, 0) (different color)
        self.assertTrue(self.logic.can_exchange_left((0, 1), 'blue', self.set_blocks))
        # Block at (0, 0) cannot exchange left (out of bounds)
        self.assertFalse(self.logic.can_exchange_left((0, 0), 'red', self.set_blocks))
        # Block at (0, 1) can exchange right with (0, 2) (different color)
        self.assertTrue(self.logic.can_exchange_right((0, 1), 'blue', self.set_blocks, self.grid_size))
        # Block at (0, 2) cannot exchange right (out of bounds)
        self.assertFalse(self.logic.can_exchange_right((0, 2), 'red', self.set_blocks, self.grid_size))

    def test_update_block(self):
        updated = self.logic.update_block((0, 0), (2, 2), self.set_blocks.copy())
        self.assertIn((2, 2), updated)
        self.assertNotIn((0, 0), updated)

    def test_exchange_block(self):
        updated = self.logic.exchange_block((0, 0), (0, 1), self.set_blocks.copy())
        self.assertEqual(updated[(0, 0)].color, 'blue')
        self.assertEqual(updated[(0, 1)].color, 'red')

    def test_has_matches_and_find_matches(self):
        # There is a horizontal match in row 1
        self.assertTrue(self.logic.has_matches(self.set_blocks))
        matches = self.logic.find_matches(self.set_blocks)
        self.assertTrue(any(pos in matches for pos in [(1, 0), (1, 1), (1, 2)]))

    def test_delete_matches(self):
        matches = {(1, 0), (1, 1), (1, 2)}
        updated = self.logic.delete_matches(self.set_blocks, matches)
        self.assertNotIn((1, 0), updated)
        self.assertNotIn((1, 1), updated)
        self.assertNotIn((1, 2), updated)

    def test_is_aligned(self):
        block1 = MagicMock(color='red')
        block2 = MagicMock(color='red')
        self.assertTrue(self.logic.is_aligned((0, 0), (0, 1), block1, block2, True))
        self.assertFalse(self.logic.is_aligned((0, 0), (1, 0), block1, block2, True))
        self.assertTrue(self.logic.is_aligned((0, 0), (1, 0), block1, block2, False))

    def test_has_gravity_and_apply_gravity(self):
        # Block at (0, 0) should fall to (2, 0)
        set_blocks = {(0, 0): MagicMock(color='red')}
        new_set_blocks = self.logic.apply_gravity(set_blocks, self.grid_size)
        self.assertIn((2, 0), new_set_blocks)
        self.assertNotIn((0, 0), new_set_blocks)
        self.assertTrue(self.logic.has_gravity(set_blocks, self.grid_size))

    def test_apply_gravity_and_eliminate_matches(self):
        # Should eliminate the horizontal match and apply gravity
        set_blocks = {
            (0, 0): MagicMock(color='red'),
            (0, 1): MagicMock(color='red'),
            (0, 2): MagicMock(color='red')
        }
        result = self.logic.apply_gravity_and_eliminate_matches(set_blocks, self.grid_size)
        self.assertEqual(result, {})

    def test_make_move_and_simple_exchange(self):
        set_blocks = {
            (2, 1): MagicMock(color='red'),
            (2, 2): MagicMock(color='blue')
        }
        # Simple move left
        updated = self.logic.make_move("move_left", (2, 2), set_blocks.copy())
        self.assertIn((2, 1), updated)
        # Exchange right
        updated = self.logic.make_move("exchange_right", (2, 1), set_blocks.copy())
        self.assertEqual(updated[(2, 1)].color, 'blue')
        self.assertEqual(updated[(2, 2)].color, 'red')

    def test_get_game_state(self):
        # Empty set_blocks = victory
        self.assertEqual(self.logic.get_game_state({}, self.colors), 3)
        # Not enough blocks of each color = defeat
        set_blocks = {(0, 0): MagicMock(color='red'), (0, 1): MagicMock(color='blue')}
        self.assertEqual(self.logic.get_game_state(set_blocks, self.colors), 2)
        # Otherwise, in progress
        set_blocks = {
            (0, 0): MagicMock(color='red'),
            (0, 1): MagicMock(color='blue'),
            (1, 0): MagicMock(color='red'),
            (1, 1): MagicMock(color='blue'),
            (2, 0): MagicMock(color='red'),
            (2, 1): MagicMock(color='blue')
        }
        self.assertEqual(self.logic.get_game_state(set_blocks, self.colors), 1)

    def test_count_block_colors(self):
        set_blocks = {
            (0, 0): MagicMock(color='red'),
            (0, 1): MagicMock(color='blue'),
            (1, 0): MagicMock(color='red')
        }
        counts = self.logic.count_block_colors(set_blocks)
        self.assertEqual(counts['red'], 2)
        self.assertEqual(counts['blue'], 1)

if __name__ == '__main__':
    unittest.main()