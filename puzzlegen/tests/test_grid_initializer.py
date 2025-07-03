import unittest
from unittest.mock import patch, MagicMock
from puzzlegen.core.grid_initializer import GridInitializer

class TestGridInitializer(unittest.TestCase):
    def setUp(self):
        self.grid_size = (5, 5)
        self.nb_blocks = 6
        self.colors = ['red', 'blue']
        self.min_nb_moves = 2
        self.stack_probability = 0.5
        self.blocks_gap = 1
        self.grid_init = GridInitializer(
            self.grid_size, self.nb_blocks, self.colors,
            self.min_nb_moves, self.stack_probability, self.blocks_gap
        )

    def test_is_valid_position(self):
        self.assertTrue(self.grid_init.is_valid_position(0, 0))
        self.assertTrue(self.grid_init.is_valid_position(4, 4))
        self.assertFalse(self.grid_init.is_valid_position(-1, 0))
        self.assertFalse(self.grid_init.is_valid_position(0, 5))

    def test_is_block_present_and_similar_block(self):
        self.grid_init.set_blocks = {(2, 2): MagicMock(color='red')}
        self.assertEqual(self.grid_init.is_block_present(2, 2), [True, 'red'])
        self.assertEqual(self.grid_init.is_block_present(1, 1), [False, None])
        self.assertTrue(self.grid_init.is_similar_block(2, 2, 'red'))
        self.assertFalse(self.grid_init.is_similar_block(2, 2, 'blue'))

    def test_check_valid_placement(self):
        self.grid_init.set_blocks = {
            (2, 2): MagicMock(color='red'),
            (3, 2): MagicMock(color='red'),
            (4, 2): MagicMock(color='red')
        }
        # Should be False if would create a vertical match
        self.assertFalse(self.grid_init.check_valid_placement(1, 2, 'red'))
        # Should be True if no match
        self.assertTrue(self.grid_init.check_valid_placement(0, 0, 'blue'))

    def test_get_highest_positions(self):
        self.grid_init.set_blocks = {
            (4, 0): MagicMock(color='red'),
            (2, 0): MagicMock(color='blue'),
            (3, 1): MagicMock(color='red')
        }
        highest = self.grid_init.get_highest_positions()
        self.assertIn((2, 0), highest)
        self.assertIn((3, 1), highest)

    def test_select_random_highest_position_and_empty_positions_with_gap(self):
        self.grid_init.set_blocks = {
            (4, 0): MagicMock(color='red'),
            (3, 1): MagicMock(color='blue')
        }
        pos = self.grid_init.select_random_highest_position()
        self.assertIsInstance(pos, tuple)
        pos2 = self.grid_init.select_empty_positions_with_gap()
        self.assertIsInstance(pos2, tuple)

    @patch('puzzlegen.core.grid_initializer.assign_blocks_per_color')
    @patch('puzzlegen.core.grid_initializer.Block')
    def test_initialize_grid(self, MockBlock, mock_assign_blocks):
        mock_assign_blocks.return_value = [('red', 3), ('blue', 3)]
        MockBlock.side_effect = lambda color: MagicMock(color=color)
        self.grid_init.initialize_grid()
        self.assertEqual(len(self.grid_init.set_blocks), self.nb_blocks)

    def test_change_set_blocks(self):
        new_blocks = {(0, 0): MagicMock(color='red')}
        self.grid_init.change_set_blocks(new_blocks)
        self.assertEqual(self.grid_init.set_blocks, new_blocks)

    def test_init_graphical_grid(self):
        set_blocks = {(0, 0): MagicMock(color='red')}
        fig, ax, grid = GridInitializer.init_graphical_grid(set_blocks, (2, 2))
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(len(grid), 2)

if __name__ == '__main__':
    unittest.main()