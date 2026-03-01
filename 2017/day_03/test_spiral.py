import unittest
from spiral import find_distance, find_first_larger, read_input, solve

import os

class TestSpiral(unittest.TestCase):
    def test_part1_distance(self):
        """Test Manhattan distance for various goal values."""
        self.assertEqual(find_distance(1), 0)
        self.assertEqual(find_distance(12), 3)
        self.assertEqual(find_distance(23), 2)
        self.assertEqual(find_distance(1024), 31)

    def test_part2_first_larger(self):
        """Test finding the first value larger than goal."""
        self.assertEqual(find_first_larger(1), 2)
        self.assertEqual(find_first_larger(2), 4)
        self.assertEqual(find_first_larger(747), 806)

    def test_solve(self):
        """Test the solve function returns a tuple of results."""
        res = solve(1024)
        self.assertEqual(res, (31, 1968))  # 1024 part 2 is 1968

    def test_read_input(self):
        """Test reading input from a temporary file."""
        test_file = "test_input.txt"
        with open(test_file, "w") as f:
            f.write("1024")
        try:
            val = read_input(test_file)
            self.assertEqual(val, 1024)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

    def test_read_input_empty(self):
        """Test that read_input raises ValueError for empty file."""
        test_file = "empty_input.txt"
        with open(test_file, "w") as f:
            f.write("")
        try:
            with self.assertRaises(ValueError):
                read_input(test_file)
        finally:
            if os.path.exists(test_file):
                os.remove(test_file)

if __name__ == '__main__':
    unittest.main()
