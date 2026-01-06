import unittest
from code import get_code

class TestCodes(unittest.TestCase):
    """Test cases for the Day 25 code generator."""

    def test_grid_values(self):
        """Verify the code generator against the provided 6x6 grid of values."""
        # Keys are (row, col) tuples, values are the expected codes.
        expected_grid = {
            (1, 1): 20151125, (1, 2): 18749137, (1, 3): 17289845, (1, 4): 30943339, (1, 5): 10071777, (1, 6): 33511524,
            (2, 1): 31916031, (2, 2): 21629792, (2, 3): 16929656, (2, 4): 7726640,  (2, 5): 15514188, (2, 6): 4041754,
            (3, 1): 16080970, (3, 2): 8057251,  (3, 3): 1601130,  (3, 4): 7981243,  (3, 5): 11661866, (3, 6): 16474243,
            (4, 1): 24592653, (4, 2): 32451966, (4, 3): 21345942, (4, 4): 9380097,  (4, 5): 10600672, (4, 6): 31527494,
            (5, 1): 77061,    (5, 2): 17552253, (5, 3): 28094349, (5, 4): 6899651,  (5, 5): 9250759,  (5, 6): 31663883,
            (6, 1): 33071741, (6, 2): 6796745,  (6, 3): 25397450, (6, 4): 24659492, (6, 5): 1534922,  (6, 6): 27995004,
        }
        
        for (row, col), expected in expected_grid.items():
            with self.subTest(row=row, col=col):
                self.assertEqual(get_code(row, col), expected)

if __name__ == "__main__":
    unittest.main()
