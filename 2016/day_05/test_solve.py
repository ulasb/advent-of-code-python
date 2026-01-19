import unittest
from solve import part1, part2

class TestDay05(unittest.TestCase):
    def test_example_part1(self):
        """Test Part 1 with the example door ID 'abc'."""
        self.assertEqual(part1("abc"), "18f47a30")

    def test_example_part2(self):
        """Test Part 2 with the example door ID 'abc'."""
        self.assertEqual(part2("abc"), "05ace8e3")

if __name__ == "__main__":
    unittest.main()
