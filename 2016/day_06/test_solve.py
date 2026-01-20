import unittest
from solve import solve_part1, solve_part2, parse_input


class TestSolve(unittest.TestCase):
    def setUp(self):
        self.test_input = [
            "eedadn",
            "drvtee",
            "eandsr",
            "raavrd",
            "atevrs",
            "tsrnev",
            "sdttsa",
            "rasrtv",
            "nssdts",
            "ntnada",
            "svetve",
            "tesnvt",
            "vntsnd",
            "vrdear",
            "dvrsen",
            "enarar",
        ]
        self.chars = parse_input(self.test_input)

    def test_part1(self):
        self.assertEqual(solve_part1(self.chars), "easter")

    def test_part2(self):
        self.assertEqual(solve_part2(self.chars), "advent")


if __name__ == "__main__":
    unittest.main()
