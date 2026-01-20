import unittest
from collections import Counter, defaultdict
from solve import solve_part1, solve_part2

class TestSolve(unittest.TestCase):
    def setUp(self):
        self.test_input = [
            "eedadn", "drvtee", "eandsr", "raavrd", "atevrs", "tsrnev", "sdttsa", 
            "rasrtv", "nssdts", "ntnada", "svetve", "tesnvt", "vntsnd", "vrdear", 
            "dvrsen", "enarar"
        ]
        self.chars = defaultdict(Counter)
        for line in self.test_input:
            for i, char in enumerate(line):
                self.chars[i][char] += 1

    def test_part1(self):
        self.assertEqual(solve_part1(self.chars), "easter")

    def test_part2(self):
        self.assertEqual(solve_part2(self.chars), "advent")

if __name__ == "__main__":
    unittest.main()
