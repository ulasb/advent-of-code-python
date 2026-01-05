#!/usr/bin/env python3

import unittest
from solution import (
    Reindeer,
    parse_reindeer_line,
    simulate_race,
    simulate_race_with_points,
    simulate_second
)


class TestReindeerRace(unittest.TestCase):
    """Unit tests for the reindeer race solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.comet_line = "Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds."
        self.dancer_line = "Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."

        self.comet = Reindeer("Comet", 14, 10, 127)
        self.dancer = Reindeer("Dancer", 16, 11, 162)
        self.example_reindeer = [self.comet, self.dancer]

    def test_parse_reindeer_line_comet(self):
        """Test parsing Comet's reindeer line."""
        reindeer = parse_reindeer_line(self.comet_line)
        self.assertEqual(reindeer.name, "Comet")
        self.assertEqual(reindeer.speed, 14)
        self.assertEqual(reindeer.fly_time, 10)
        self.assertEqual(reindeer.rest_time, 127)

    def test_parse_reindeer_line_dancer(self):
        """Test parsing Dancer's reindeer line."""
        reindeer = parse_reindeer_line(self.dancer_line)
        self.assertEqual(reindeer.name, "Dancer")
        self.assertEqual(reindeer.speed, 16)
        self.assertEqual(reindeer.fly_time, 11)
        self.assertEqual(reindeer.rest_time, 162)

    def test_reindeer_initial_state(self):
        """Test that reindeer start in correct initial state."""
        reindeer = Reindeer("Test", 10, 5, 3)
        self.assertEqual(reindeer.distance, 0)
        self.assertEqual(reindeer.points, 0)
        self.assertTrue(reindeer.flying)
        self.assertEqual(reindeer.time_in_current_state, 0)

    def test_reindeer_reset(self):
        """Test reindeer reset functionality."""
        reindeer = Reindeer("Test", 10, 5, 3)
        # Modify state
        reindeer.distance = 100
        reindeer.points = 50
        reindeer.flying = False
        reindeer.time_in_current_state = 7

        reindeer.reset()

        self.assertEqual(reindeer.distance, 0)
        self.assertEqual(reindeer.points, 0)
        self.assertTrue(reindeer.flying)
        self.assertEqual(reindeer.time_in_current_state, 0)

    def test_simulate_second_basic(self):
        """Test basic second simulation."""
        reindeer = Reindeer("Test", 10, 2, 1)
        simulate_second([reindeer], award_points=False)

        self.assertEqual(reindeer.distance, 10)
        self.assertEqual(reindeer.time_in_current_state, 1)
        self.assertTrue(reindeer.flying)

    def test_simulate_second_with_points(self):
        """Test second simulation with point awarding."""
        reindeer1 = Reindeer("Fast", 20, 5, 5)
        reindeer2 = Reindeer("Slow", 10, 5, 5)

        simulate_second([reindeer1, reindeer2], award_points=True)

        # Fast reindeer should be in lead and get a point
        self.assertEqual(reindeer1.distance, 20)
        self.assertEqual(reindeer1.points, 1)
        self.assertEqual(reindeer2.distance, 10)
        self.assertEqual(reindeer2.points, 0)

    def test_simulate_second_tie_points(self):
        """Test that tied reindeer both get points."""
        reindeer1 = Reindeer("Reindeer1", 10, 5, 5)
        reindeer2 = Reindeer("Reindeer2", 10, 5, 5)

        simulate_second([reindeer1, reindeer2], award_points=True)

        # Both should get points since they're tied
        self.assertEqual(reindeer1.points, 1)
        self.assertEqual(reindeer2.points, 1)

    def test_part1_example_after_1_second(self):
        """Test part 1 example: positions after 1 second."""
        max_distance = simulate_race(self.example_reindeer, 1)

        # Comet: 14 km, Dancer: 16 km, max should be 16
        self.assertEqual(max_distance, 16)

        # Verify individual distances
        self.assertEqual(self.comet.distance, 14)
        self.assertEqual(self.dancer.distance, 16)

    def test_part1_example_after_10_seconds(self):
        """Test part 1 example: positions after 10 seconds."""
        max_distance = simulate_race(self.example_reindeer, 10)

        # Comet: 140 km, Dancer: 160 km, max should be 160
        self.assertEqual(max_distance, 160)

        comet_distance = next(r.distance for r in self.example_reindeer if r.name == "Comet")
        dancer_distance = next(r.distance for r in self.example_reindeer if r.name == "Dancer")

        self.assertEqual(comet_distance, 140)
        self.assertEqual(dancer_distance, 160)

    def test_part1_example_after_11_seconds(self):
        """Test part 1 example: positions after 11 seconds."""
        max_distance = simulate_race(self.example_reindeer, 11)

        # Comet: still 140 km (resting), Dancer: 176 km, max should be 176
        self.assertEqual(max_distance, 176)

        comet_distance = next(r.distance for r in self.example_reindeer if r.name == "Comet")
        dancer_distance = next(r.distance for r in self.example_reindeer if r.name == "Dancer")

        self.assertEqual(comet_distance, 140)
        self.assertEqual(dancer_distance, 176)

    def test_part1_example_after_1000_seconds(self):
        """Test part 1 example: positions after 1000 seconds."""
        max_distance = simulate_race(self.example_reindeer, 1000)

        # Comet should be at 1120 km, Dancer at 1056 km, Comet wins
        self.assertEqual(max_distance, 1120)

        comet_distance = next(r.distance for r in self.example_reindeer if r.name == "Comet")
        dancer_distance = next(r.distance for r in self.example_reindeer if r.name == "Dancer")

        self.assertEqual(comet_distance, 1120)
        self.assertEqual(dancer_distance, 1056)

    def test_part2_example_after_1_second(self):
        """Test part 2 example: points after 1 second."""
        max_points = simulate_race_with_points(self.example_reindeer, 1)

        # Dancer is in lead after 1 second and gets 1 point
        self.assertEqual(max_points, 1)

        comet_points = next(r.points for r in self.example_reindeer if r.name == "Comet")
        dancer_points = next(r.points for r in self.example_reindeer if r.name == "Dancer")

        self.assertEqual(comet_points, 0)  # Comet not in lead
        self.assertEqual(dancer_points, 1)  # Dancer in lead

    def test_part2_example_after_140_seconds(self):
        """Test part 2 example: points after 140 seconds."""
        max_points = simulate_race_with_points(self.example_reindeer, 140)

        # After 140 seconds, Comet pulls into lead and gets first point
        # Dancer had been in lead for 139 seconds, so has 139 points
        dancer_points = next(r.points for r in self.example_reindeer if r.name == "Dancer")
        self.assertEqual(dancer_points, 139)

        comet_points = next(r.points for r in self.example_reindeer if r.name == "Comet")
        self.assertEqual(comet_points, 1)

    def test_part2_example_after_1000_seconds(self):
        """Test part 2 example: final points after 1000 seconds."""
        max_points = simulate_race_with_points(self.example_reindeer, 1000)

        # Dancer should have 689 points, Comet should have 312 points
        self.assertEqual(max_points, 689)

        comet_points = next(r.points for r in self.example_reindeer if r.name == "Comet")
        dancer_points = next(r.points for r in self.example_reindeer if r.name == "Dancer")

        self.assertEqual(comet_points, 312)
        self.assertEqual(dancer_points, 689)


if __name__ == "__main__":
    unittest.main()
