import unittest
from maze import is_wall, count_moves, count_rooms, FAVORITE_NUMBER


class TestMaze(unittest.TestCase):
    def test_example_shortest_path(self):
        """Test the example case with FAVORITE_NUMBER=10."""
        from unittest.mock import patch
        import maze

        # Clear cache after the test to prevent side effects
        self.addCleanup(maze.is_wall.cache_clear)

        with patch("maze.FAVORITE_NUMBER", 10):
            maze.is_wall.cache_clear()  # Clear cache for the new constant
            moves = count_moves((1, 1), (7, 4))
            self.assertEqual(moves, 11)

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
