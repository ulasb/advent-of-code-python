#!/usr/bin/env python3
"""
Advent of Code 2015 - Day 14: Reindeer Olympics

This script simulates reindeer races to find winners based on distance traveled
and points earned for being in the lead during each second of the race.
"""

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from typing import List

# Constants
REINDEER_PATTERN = r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds'
RACE_DURATION = 2503
DEFAULT_INPUT_FILE = "input.txt"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@dataclass
class Reindeer:
    """
    Represents a reindeer with flying and resting characteristics.

    Attributes
    ----------
    name : str
        The reindeer's name
    speed : int
        Speed in km/s when flying
    fly_time : int
        Number of seconds the reindeer can fly before needing to rest
    rest_time : int
        Number of seconds the reindeer must rest before flying again
    distance : int
        Current distance traveled (default: 0)
    points : int
        Points earned in point-based scoring (default: 0)
    flying : bool
        Whether the reindeer is currently flying (default: True)
    time_in_current_state : int
        Seconds spent in current flying/resting state (default: 0)
    """
    name: str
    speed: int
    fly_time: int
    rest_time: int
    distance: int = 0
    points: int = 0
    flying: bool = True
    time_in_current_state: int = 0

    def reset(self) -> None:
        """Reset reindeer state for a new race."""
        self.distance = 0
        self.points = 0
        self.flying = True
        self.time_in_current_state = 0

    def update_position(self) -> None:
        """Update reindeer position and state for one second."""
        if self.flying:
            self.distance += self.speed
            self.time_in_current_state += 1

            # Check if we need to switch to resting
            if self.time_in_current_state >= self.fly_time:
                self.flying = False
                self.time_in_current_state = 0
        else:
            self.time_in_current_state += 1

            # Check if we need to switch to flying
            if self.time_in_current_state >= self.rest_time:
                self.flying = True
                self.time_in_current_state = 0


def parse_reindeer_line(line: str) -> Reindeer:
    """
    Parse a line of reindeer data and return a Reindeer object.

    Parameters
    ----------
    line : str
        Input line in format: "Name can fly X km/s for Y seconds, but then must rest for Z seconds."

    Returns
    -------
    Reindeer
        Parsed reindeer object

    Raises
    ------
    ValueError
        If the line format is invalid
    """
    match = re.match(REINDEER_PATTERN, line.strip())

    if not match:
        raise ValueError(f"Invalid line format: {line}")

    name, speed, fly_time, rest_time = match.groups()
    return Reindeer(name, int(speed), int(fly_time), int(rest_time))


def read_input_file(filename: str = DEFAULT_INPUT_FILE) -> List[Reindeer]:
    """
    Read the input file and return a list of Reindeer objects.

    Parameters
    ----------
    filename : str, optional
        Path to the input file (default: "input.txt")

    Returns
    -------
    List[Reindeer]
        List of parsed reindeer objects

    Raises
    ------
    FileNotFoundError
        If the input file doesn't exist
    ValueError
        If any line in the input file has invalid format
    """
    reindeer_list = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # Skip empty lines
                reindeer = parse_reindeer_line(line)
                reindeer_list.append(reindeer)

    return reindeer_list


def simulate_second(reindeer_list: List[Reindeer], award_points: bool = False) -> None:
    """
    Simulate one second of the race for all reindeer.

    Parameters
    ----------
    reindeer_list : List[Reindeer]
        List of reindeer participating in the race
    award_points : bool, optional
        Whether to award points to reindeer in the lead (default: False)
    """
    # Update all positions for this second
    for reindeer in reindeer_list:
        reindeer.update_position()

    if award_points:
        # Find the current maximum distance
        current_max_distance = max(reindeer.distance for reindeer in reindeer_list)

        # Award points to all reindeer at the current maximum distance
        for reindeer in reindeer_list:
            if reindeer.distance == current_max_distance:
                reindeer.points += 1


def run_race_simulation(reindeer_list: List[Reindeer], total_seconds: int, award_points: bool = False) -> None:
    """
    Run the race simulation for the specified duration.

    Parameters
    ----------
    reindeer_list : List[Reindeer]
        List of reindeer participating in the race
    total_seconds : int
        Duration of the race in seconds
    award_points : bool, optional
        Whether to award points to leaders each second (default: False)
    """
    # Reset all reindeer to initial state
    for reindeer in reindeer_list:
        reindeer.reset()

    # Run simulation
    for _ in range(total_seconds):
        simulate_second(reindeer_list, award_points=award_points)


def simulate_race(reindeer_list: List[Reindeer], total_seconds: int) -> int:
    """
    Simulate the race for given seconds and return the max distance traveled.

    Parameters
    ----------
    reindeer_list : List[Reindeer]
        List of reindeer participating in the race
    total_seconds : int
        Duration of the race in seconds

    Returns
    -------
    int
        Maximum distance traveled by any reindeer
    """
    run_race_simulation(reindeer_list, total_seconds, award_points=False)
    return max(reindeer.distance for reindeer in reindeer_list)


def simulate_race_with_points(reindeer_list: List[Reindeer], total_seconds: int) -> int:
    """
    Simulate the race for given seconds and return the max points earned.

    Parameters
    ----------
    reindeer_list : List[Reindeer]
        List of reindeer participating in the race
    total_seconds : int
        Duration of the race in seconds

    Returns
    -------
    int
        Maximum points earned by any reindeer
    """
    run_race_simulation(reindeer_list, total_seconds, award_points=True)
    return max(reindeer.points for reindeer in reindeer_list)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns
    -------
    argparse.Namespace
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Advent of Code 2015 - Day 14: Find winning reindeer in distance and points races",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 solution.py                    # Use default input.txt
  python3 solution.py -f custom.txt     # Use custom input file
  python3 solution.py --test           # Run unit tests
        """
    )

    parser.add_argument(
        '-f', '--file',
        type=str,
        default=DEFAULT_INPUT_FILE,
        help=f'Input file containing reindeer statements (default: {DEFAULT_INPUT_FILE})'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='Run unit tests instead of main program'
    )

    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    """
    Main function to run the reindeer race simulations.

    Parameters
    ----------
    args : argparse.Namespace
        Parsed command-line arguments
    """
    try:
        logger.info(f"Reading reindeer data from {args.file}")
        reindeer_list = read_input_file(args.file)

        logger.info(f"Loaded {len(reindeer_list)} reindeer:")
        for reindeer in reindeer_list:
            logger.info(f"  {reindeer.name}: {reindeer.speed} km/s for {reindeer.fly_time}s, rest {reindeer.rest_time}s")

        # Part 1: Distance-based winner
        logger.info("Running Part 1: Distance-based race...")
        max_distance = simulate_race(reindeer_list, RACE_DURATION)
        logger.info(f"Part 1 - After {RACE_DURATION} seconds, the winning reindeer traveled {max_distance} km!")

        # Part 2: Points-based winner
        logger.info("Running Part 2: Points-based race...")
        max_points = simulate_race_with_points(reindeer_list, RACE_DURATION)
        logger.info(f"Part 2 - After {RACE_DURATION} seconds, the winning reindeer earned {max_points} points!")

    except FileNotFoundError:
        logger.error(f"Input file '{args.file}' not found.")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Invalid input format: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_arguments()

    if args.test:
        # Run unit tests from test_solution.py
        import subprocess
        import sys
        result = subprocess.run([sys.executable, '-m', 'unittest', 'test_solution.py', '-v'])
        sys.exit(result.returncode)
    else:
        main(args)
