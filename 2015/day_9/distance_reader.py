#!/usr/bin/env python3
"""
Advent of Code 2015 Day 9 - Distance Reader

Reads a file containing distances between cities and stores them efficiently
for quick lookups of cities and distances. Solves the Traveling Salesman Problem
using dynamic programming to find both shortest and longest routes.
"""

import argparse
import re
import sys
import unittest
from typing import Dict, List, Optional, Set, Tuple

# Constants
INF = float('inf')
NEG_INF = float('-inf')

# Regex pattern for parsing distance lines: "City1 to City2 = distance"
DISTANCE_PATTERN = re.compile(r'^(\w+)\s+to\s+(\w+)\s+=\s+(\d+)$')


class DistanceGraph:
    """
    Efficient graph representation for city distances.

    Uses a dictionary of dictionaries for O(1) distance lookups.
    Supports bidirectional distances and provides TSP solving capabilities.
    """

    def __init__(self):
        """Initialize empty distance graph."""
        self.distances: Dict[str, Dict[str, int]] = {}
        self.cities: Set[str] = set()

    def parse_line(self, line: str) -> None:
        """
        Parse a single line in the format: "City1 to City2 = distance"

        Args:
            line: Input line to parse

        Returns:
            True if line was parsed successfully, False otherwise

        Raises:
            ValueError: If line format is invalid
        """
        line = line.strip()
        if not line:
            return True  # Empty lines are OK

        match = DISTANCE_PATTERN.match(line)
        if not match:
            raise ValueError(f"Invalid format: expected 'City1 to City2 = distance', got: {line}")

        city1, city2, distance_str = match.groups()
        distance = int(distance_str)

        # Add both directions since distances are bidirectional
        self.distances.setdefault(city1, {})
        self.distances.setdefault(city2, {})

        self.distances[city1][city2] = distance
        self.distances[city2][city1] = distance

        # Add cities to set
        self.cities.add(city1)
        self.cities.add(city2)

        return True

    def load_from_file(self, filename: str) -> None:
        """
        Load distances from a file.

        Args:
            filename: Path to the input file

        Raises:
            FileNotFoundError: If file doesn't exist
            IOError: If file cannot be read
            ValueError: If any line has invalid format
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    try:
                        self.parse_line(line)
                    except ValueError as e:
                        raise ValueError(f"Line {line_num}: {e}") from e
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{filename}' not found")
        except IOError as e:
            raise IOError(f"Error reading file '{filename}': {e}") from e

    def load_from_lines(self, lines: List[str]) -> None:
        """
        Load distances from a list of strings (useful for testing).

        Args:
            lines: List of distance strings

        Raises:
            ValueError: If any line has invalid format
        """
        for line_num, line in enumerate(lines, 1):
            try:
                self.parse_line(line)
            except ValueError as e:
                raise ValueError(f"Line {line_num}: {e}") from e

    def get_cities(self) -> List[str]:
        """Get sorted list of all cities."""
        return sorted(self.cities)

    def get_distance(self, city1: str, city2: str) -> int:
        """
        Get distance between two cities.

        Args:
            city1: First city
            city2: Second city

        Returns:
            Distance between cities

        Raises:
            KeyError: If cities don't exist or no direct distance
        """
        if city1 not in self.distances:
            raise KeyError(f"City '{city1}' not found")
        if city2 not in self.distances[city1]:
            raise KeyError(f"No distance found between '{city1}' and '{city2}'")
        return self.distances[city1][city2]

    def solve_tsp(self) -> Tuple[Optional[int], Optional[int]]:
        """
        Solve Traveling Salesman Problem using dynamic programming.

        Finds both shortest and longest complete routes visiting all cities exactly once.

        Returns:
            Tuple of (shortest_distance, longest_distance), or (None, None) if no route exists

        Time Complexity: O(n² × 2^n) - acceptable for n ≤ 20
        Space Complexity: O(n × 2^n) for DP tables
        """
        if not self.cities:
            return None, None

        city_list = self.get_cities()
        n = len(city_list)

        # Single DP table: store both min and max as tuples
        dp = [[None] * (1 << n) for _ in range(n)]  # (min_cost, max_cost)

        def tsp_dp(current_idx: int, visited_mask: int) -> Tuple[float, float]:
            """Return (min_cost, max_cost) for TSP subproblem."""
            if visited_mask == (1 << n) - 1:  # All cities visited
                return 0.0, 0.0

            if dp[current_idx][visited_mask] is not None:
                return dp[current_idx][visited_mask]

            min_cost = INF
            max_cost = NEG_INF
            current_city = city_list[current_idx]

            # Try all unvisited cities
            for next_idx in range(n):
                if not (visited_mask & (1 << next_idx)):
                    next_city = city_list[next_idx]
                    if next_city in self.distances[current_city]:
                        distance = self.distances[current_city][next_city]
                        next_min, next_max = tsp_dp(next_idx, visited_mask | (1 << next_idx))

                        min_cost = min(min_cost, distance + next_min)
                        max_cost = max(max_cost, distance + next_max)

            dp[current_idx][visited_mask] = (min_cost, max_cost)
            return min_cost, max_cost

        # Find best routes from each starting city
        overall_min = INF
        overall_max = NEG_INF

        for start_idx in range(n):
            min_dist, max_dist = tsp_dp(start_idx, 1 << start_idx)
            overall_min = min(overall_min, min_dist)
            overall_max = max(overall_max, max_dist)

        if overall_min == INF or overall_max == NEG_INF:
            return None, None

        return int(overall_min), int(overall_max)

    def __len__(self) -> int:
        """Return number of cities."""
        return len(self.cities)

    def __str__(self) -> str:
        """String representation."""
        num_distances = sum(len(distances) for distances in self.distances.values()) // 2
        return f"DistanceGraph: {len(self.cities)} cities, {num_distances} unique distances"


class TestDistanceReader(unittest.TestCase):
    """Unit tests for the distance reader functionality."""

    def test_sample_data(self):
        """Test with the provided sample data."""
        graph = DistanceGraph()
        sample_data = [
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141"
        ]

        graph.load_from_lines(sample_data)

        # Verify cities were loaded correctly
        expected_cities = ["Belfast", "Dublin", "London"]  # sorted
        self.assertEqual(graph.get_cities(), expected_cities)

        # Verify distances were loaded correctly
        self.assertEqual(graph.get_distance("London", "Dublin"), 464)
        self.assertEqual(graph.get_distance("London", "Belfast"), 518)
        self.assertEqual(graph.get_distance("Dublin", "Belfast"), 141)

        # Verify bidirectional distances
        self.assertEqual(graph.get_distance("Dublin", "London"), 464)
        self.assertEqual(graph.get_distance("Belfast", "London"), 518)
        self.assertEqual(graph.get_distance("Belfast", "Dublin"), 141)

    def test_shortest_and_longest_routes(self):
        """Test that shortest and longest routes are calculated correctly."""
        graph = DistanceGraph()
        sample_data = [
            "London to Dublin = 464",
            "London to Belfast = 518",
            "Dublin to Belfast = 141"
        ]

        graph.load_from_lines(sample_data)

        # Run the TSP algorithm
        min_distance, max_distance = graph.solve_tsp()

        # Verify results
        self.assertEqual(min_distance, 605)  # Shortest route
        self.assertEqual(max_distance, 982)  # Longest route


    def test_empty_graph(self):
        """Test behavior with empty graph."""
        graph = DistanceGraph()
        min_dist, max_dist = graph.solve_tsp()
        self.assertIsNone(min_dist)
        self.assertIsNone(max_dist)

    def test_invalid_line_format(self):
        """Test error handling for invalid line formats."""
        graph = DistanceGraph()

        with self.assertRaises(ValueError):
            graph.parse_line("Invalid format")

        with self.assertRaises(ValueError):
            graph.parse_line("London Dublin 464")  # Missing 'to' and '='

        with self.assertRaises(ValueError):
            graph.parse_line("London to Dublin = abc")  # Non-numeric distance

    def test_distance_lookup_errors(self):
        """Test error handling for distance lookups."""
        graph = DistanceGraph()
        graph.load_from_lines(["London to Dublin = 464"])

        # Valid lookup
        self.assertEqual(graph.get_distance("London", "Dublin"), 464)

        # Invalid city
        with self.assertRaises(KeyError):
            graph.get_distance("London", "Paris")


def main():
    """Main entry point for the Advent of Code Day 9 solver."""
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 9: All in a Single Night"
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        default="input.txt",
        help="Input file containing city distances (default: input.txt)"
    )
    parser.add_argument(
        "--test", "-t",
        action="store_true",
        help="Run unit tests instead of processing input file"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output including graph statistics"
    )

    args = parser.parse_args()

    if args.test:
        # Run unit tests
        unittest.main(argv=[''], exit=False, verbosity=2)
        return

    # Normal execution with modern approach
    try:
        graph = DistanceGraph()
        graph.load_from_file(args.input_file)

        if args.verbose:
            print(f"Loaded {graph}")
            print(f"Cities: {', '.join(graph.get_cities())}")

        min_dist, max_dist = graph.solve_tsp()

        if min_dist is None or max_dist is None:
            print("No complete route found - cities may not be fully connected!")
            sys.exit(1)

        print(f"Shortest complete route distance: {min_dist}")
        print(f"Longest complete route distance: {max_dist}")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except (IOError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
