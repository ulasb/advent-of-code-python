"""
Tests for Advent of Code 2017, Day 7: Recursive Circus.
Created by Ulaş Bardak.
This code is published under the Mozilla Public License 2.0.
"""

import unittest
import os
from recursive_circus import solve_part_1, solve_part_2


class TestRecursiveCircus(unittest.TestCase):
    """Test cases for the Recursive Circus puzzle."""

    def setUp(self):
        """Sets up the test data."""
        self.test_filepath = "test_input.txt"
        with open(self.test_filepath, "w") as f:
            f.write(
                "pbga (66)\n"
                "xhth (57)\n"
                "ebii (61)\n"
                "havc (66)\n"
                "ktlj (57)\n"
                "fwft (72) -> ktlj, cntj, xhth\n"
                "qoyq (66)\n"
                "padx (45) -> pbga, havc, qoyq\n"
                "tknk (41) -> ugml, padx, fwft\n"
                "jptl (61)\n"
                "ugml (68) -> gyxo, ebii, jptl\n"
                "gyxo (61)\n"
                "cntj (57)\n"
            )

    def tearDown(self):
        """Cleans up the test data."""
        if os.path.exists(self.test_filepath):
            os.remove(self.test_filepath)

    def test_part_1(self):
        """Tests Part 1 with the sample input."""
        result = solve_part_1(self.test_filepath)
        self.assertEqual(result, "tknk")

    def test_part_2(self):
        """Tests Part 2 with the sample input."""
        result = solve_part_2(self.test_filepath)
        self.assertEqual(result, 60)


if __name__ == "__main__":
    unittest.main()
