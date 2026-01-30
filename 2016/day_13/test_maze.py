import unittest
from maze import is_wall, count_moves, count_rooms, FAVORITE_NUMBER


class TestMaze(unittest.TestCase):
    def test_example_shortest_path(self):
        # Using the example favorite number 10
        # The problem says target (7, 4) is 11 steps away from (1, 1)

        # We need to temporarily override FAVORITE_NUMBER or mock is_wall
        import maze

        original_val = maze.FAVORITE_NUMBER
        maze.FAVORITE_NUMBER = 10
        maze.is_wall.cache_clear()  # Clear cache for new number

        try:
            moves = count_moves((1, 1), (7, 4))
            self.assertEqual(moves, 11)
        finally:
            maze.FAVORITE_NUMBER = original_val
            maze.is_wall.cache_clear()

    def test_part1_result(self):
        # Verify our current answer for Part 1 remains consistent
        moves = count_moves((1, 1), (31, 39))
        self.assertEqual(moves, 96)

    def test_part2_result(self):
        # Verify our current answer for Part 2 remains consistent
        rooms = count_rooms((1, 1), 50)
        self.assertEqual(rooms, 141)


if __name__ == "__main__":
    unittest.main()
