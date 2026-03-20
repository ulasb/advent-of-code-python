import unittest
from solution import solve_instructions


class TestSolution(unittest.TestCase):
    """
    Unit tests for the AoC 2017 Day 8 solution.
    """

    def test_example(self):
        """
        Test the example from the puzzle description.
        """
        example_input = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10"""
        part1, part2 = solve_instructions(example_input)
        self.assertEqual(part1, 1)
        self.assertEqual(part2, 10)


if __name__ == "__main__":
    unittest.main()
