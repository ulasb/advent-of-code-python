"""
Tests for Advent of Code 2016, Day 10 solver.
Created and published by Ulaş Bardak under the Mozilla Public License 2.0.
"""

import unittest
import os
from solve import parse_input


class TestSolve(unittest.TestCase):
    """Test cases for parsing bot instructions."""

    def setUp(self):
        """Create a temporary input file for testing."""
        self.test_filename = "test_input.txt"
        with open(self.test_filename, "w", encoding="utf-8") as f:
            f.write("value 5 goes to bot 2\n")
            f.write("bot 2 gives low to bot 1 and high to bot 0\n")
            f.write("value 3 goes to bot 1\n")
            f.write("bot 1 gives low to output 1 and high to bot 0\n")
            f.write("bot 0 gives low to output 2 and high to output 0\n")
            f.write("value 2 goes to bot 2\n")

    def tearDown(self):
        """Remove the temporary input file."""
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_parsing(self):
        """Test that the holding, directions, and outputs are parsed correctly."""
        holding, directions, outputs = parse_input(self.test_filename)

        # Check holding
        # bot 2 gets value 5 and 2
        # bot 1 gets value 3
        self.assertEqual(holding[2], [5, 2])
        self.assertEqual(holding[1], [3])
        self.assertEqual(len(holding), 2)

        # Check directions (types and IDs)
        # bot 2 gives low to bot 1 and high to bot 0
        self.assertEqual(directions[2], {"low": ("bot", 1), "high": ("bot", 0)})
        # bot 1 gives low to output 1 and high to bot 0
        self.assertEqual(directions[1], {"low": ("output", 1), "high": ("bot", 0)})
        # bot 0 gives low to output 2 and high to output 0
        self.assertEqual(directions[0], {"low": ("output", 2), "high": ("output", 0)})
        self.assertEqual(len(directions), 3)

        # Check outputs (initially empty)
        self.assertEqual(len(outputs), 0)

    def test_execution(self):
        """Test the end-to-end execution of chip transfers."""
        holding, directions, outputs = parse_input(self.test_filename)
        # Import local execute_directions
        from solve import execute_directions

        execute_directions(holding, directions, outputs)

        # Tracing the chips:
        # 1. bot 2 has [5, 2]. Gives 2 to bot 1, 5 to bot 0.
        # 2. bot 1 already had [3], now has [3, 2]. Gives 2 to output 1, 3 to bot 0.
        # 3. bot 0 now has [5, 3]. Gives 3 to output 2, 5 to output 0.
        self.assertEqual(outputs[1], [2])
        self.assertEqual(outputs[2], [3])
        self.assertEqual(outputs[0], [5])
        # Bots should be empty
        self.assertEqual(holding[0], [])
        self.assertEqual(holding[1], [])
        self.assertEqual(holding[2], [])


if __name__ == "__main__":
    unittest.main()
