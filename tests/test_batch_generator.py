import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
import tempfile
import datetime

from puzzlegen.core.batch_generator import PuzzleBatchGenerator

class TestPuzzleBatchGenerator(unittest.TestCase):
    def setUp(self):
        self.blocks_range = (6, 7)
        self.colors_range = (2, 2)
        self.colors_blocks = ['red', 'blue']
        self.nb_moves = 2
        self.grid_size = (5, 5)
        self.stack_probability = 0.5
        self.generator = PuzzleBatchGenerator(
            self.blocks_range, self.colors_range, self.colors_blocks,
            self.nb_moves, self.grid_size, self.stack_probability
        )

    @patch('puzzlegen.core.batch_generator.GridInitializer')
    @patch('puzzlegen.core.batch_generator.BFSSolver')
    @patch('puzzlegen.core.batch_generator.PuzzleLogic')
    def test_generate_puzzles(self, MockPuzzleLogic, MockBFSSolver, MockGridInitializer):
        # Mock the solver to always return a solvable puzzle
        mock_solver = MockBFSSolver.return_value
        mock_solver.perform_all_blocks_moves.return_value = (True, {
            "rounds_number_history": [0, 1],
            "set_blocks_history": [{(0, 0): MagicMock(get_color=lambda: 'red')}],
            "moves_types_history": ['move_left', ''],
            "moved_blocks_history": [(0, 0), ()]
        })
        result = self.generator.generate_puzzles()
        self.assertIsInstance(result, dict)
        self.assertTrue(any(len(v) > 0 for v in result.values()))

    def test_set_batch(self):
        batch = {'solvable_in_1_moves': [("dummy_solution", (5, 5))]}
        self.generator.set_batch(batch)
        self.assertEqual(self.generator.puzzle_batch, batch)

    def test_compute_stats(self):
        self.generator.puzzle_batch = {'solvable_in_1_moves': [1, 2], 'solvable_in_2_moves': [3]}
        self.generator.compute_stats()
        self.assertEqual(self.generator.stats['solvable_in_1_moves'], 2)
        self.assertEqual(self.generator.stats['solvable_in_2_moves'], 1)

    @patch('matplotlib.pyplot.figure')
    def test_print_charts(self, mock_figure):
        self.generator.stats = {'solvable_in_1_moves': 2}
        self.generator.nb_unsolvables = 1
        # Should not raise
        self.generator.print_charts(show=False)

    @patch('matplotlib.pyplot.get_fignums', return_value=[1])
    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.backends.backend_pdf.PdfPages')
    def test_save_multi_image(self, mock_pdfpages, mock_figure, mock_get_fignums):
        mock_pdf = mock_pdfpages.return_value
        self.generator.save_multi_image("test.pdf")
        mock_pdf.close.assert_called_once()

    def test_save_results_as_csv_and_save_file(self):
        # Prepare dummy csv_data
        self.generator.csv_data = {
            "cubes": [6],
            "positions": [[(0, 0)]],
            "colors": [['red']],
            "moves": [1]
        }
        # Patch save_file to avoid actual file operations
        with patch.object(self.generator, 'save_file') as mock_save_file:
            self.generator.save_results_as_csv()
            mock_save_file.assert_called()

    @patch('builtins.print')
    def test_save_file_local(self, mock_print):
        # Create a dummy file
        with tempfile.TemporaryDirectory() as tmpdirname:
            filename = os.path.join(tmpdirname, "dummy.txt")
            with open(filename, "w") as f:
                f.write("test")
            # Patch os.path.dirname to return tmpdirname
            with patch('os.path.dirname', return_value=tmpdirname):
                self.generator.save_file(filename)
                # Check that the file was moved to outputs
                outputs_dir = os.path.abspath(os.path.join(tmpdirname, '..', '..', 'outputs'))
                self.assertTrue(os.path.exists(outputs_dir))

if __name__ == '__main__':
    unittest.main()