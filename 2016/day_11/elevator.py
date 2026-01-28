"""
Solution for Advent of Code 2016, Day 11.

Created and published by Ulaş Bardak.
This code is licensed under the Mozilla Public License 2.0.
The MPL 2.0 is a copyleft license that allows for the use, modification,
and distribution of the code, but requires that any changes to the
licensed code be made available under the same license.
"""

import sys
import re
import itertools
import unittest
from collections import deque
from typing import List, Tuple, Set


def parse_input(filename: str) -> Tuple[List[List[str]], List[List[str]]]:
    """
    Parses the input file and returns two lists.

    Parameters
    ----------
    filename : str
        The path to the input file.

    Returns
    -------
    Tuple[List[List[str]], List[List[str]]]
        A tuple containing:
        - floors_gens: List of lists, where each inner list contains generator types for that floor.
        - floors_chips: List of lists, where each inner list contains microchip types for that floor.
    """
    floors_gens: List[List[str]] = []
    floors_chips: List[List[str]] = []
    with open(filename, "r") as f:
        for line in f:
            if not line.strip():
                continue
            # Find all generators: "a strontium generator" -> "strontium"
            gens = re.findall(r"(\w+)(?:-compatible)? generator", line)
            # Find all microchips: "a strontium-compatible microchip" -> "strontium"
            chips = re.findall(r"(\w+)-compatible microchip", line)

            floors_gens.append(sorted(gens))
            floors_chips.append(sorted(chips))

    # Ensure we have 4 floors
    if len(floors_gens) > 4:
        raise ValueError(f"Input has {len(floors_gens)} floors, expected at most 4.")
    while len(floors_gens) < 4:
        floors_gens.append([])
        floors_chips.append([])

    return floors_gens, floors_chips


def print_floors(
    floors_gens: List[List[str]], floors_chips: List[List[str]], elevator_floor: int = 0
) -> None:
    """
    Prints the state of the floors.

    Parameters
    ----------
    floors_gens : List[List[str]]
        Generators on each floor.
    floors_chips : List[List[str]]
        Microchips on each floor.
    elevator_floor : int, optional
        The current floor of the elevator (0-indexed), by default 0.
    """
    for i in range(3, -1, -1):
        num = i + 1
        e_mark = "E" if elevator_floor == i else " "
        gens = ", ".join(floors_gens[i]) if floors_gens[i] else "None"
        chips = ", ".join(floors_chips[i]) if floors_chips[i] else "None"
        print(f"Floor {num} [{e_mark}]: Generators: {gens} | Microchips: {chips}")


def is_valid_floor(gens_indices: Set[int], chips_indices: Set[int]) -> bool:
    """
    Check if a floor state is valid.

    A chip is fried if it is on a floor with any generator, unless it has its own generator.

    Parameters
    ----------
    gens_indices : Set[int]
        Indices of generators on the floor.
    chips_indices : Set[int]
        Indices of microchips on the floor.

    Returns
    -------
    bool
        True if the floor state is valid, False otherwise.
    """
    if not gens_indices:
        return True
    # If there are any generators, every chip must have its corresponding generator
    for chip_idx in chips_indices:
        if chip_idx not in gens_indices:
            return False
    return True


def get_canonical(
    elevator_pos: int, gen_positions: Tuple[int, ...], chip_positions: Tuple[int, ...]
) -> Tuple[int, Tuple[Tuple[int, int], ...]]:
    """
    Returns a canonical representation of the state to handle interchangeable pairs.

    Parameters
    ----------
    elevator_pos : int
        Current floor of the elevator.
    gen_positions : Tuple[int, ...]
        Positions (floors) of each generator.
    chip_positions : Tuple[int, ...]
        Positions (floors) of each microchip.

    Returns
    -------
    Tuple[int, Tuple[Tuple[int, int], ...]]
        A canonical representation of the state.
    """
    pairs = sorted(zip(gen_positions, chip_positions))
    return (elevator_pos, tuple(pairs))


def solve(floors_gens: List[List[str]], floors_chips: List[List[str]]) -> int:
    """
    Finds the minimum number of steps to move all items to the fourth floor.

    Uses Breadth-First Search (BFS) with symmetry breaking.

    Parameters
    ----------
    floors_gens : List[List[str]]
        Initial generators on each floor.
    floors_chips : List[List[str]]
        Initial microchips on each floor.

    Returns
    -------
    int
        The minimum number of steps, or -1 if no solution is found.
    """
    # Collect all unique types and map them to indices
    all_types: Set[str] = set()
    for floor in floors_gens:
        for t in floor:
            all_types.add(t)
    for floor in floors_chips:
        for t in floor:
            all_types.add(t)

    all_types_list = sorted(list(all_types))
    type_to_idx = {t: i for i, t in enumerate(all_types_list)}
    num_types = len(all_types_list)

    # State: (elevator_pos, tuple(gen_positions), tuple(chip_positions))
    initial_gen_pos = [0] * num_types
    initial_chip_pos = [0] * num_types

    for f, gens in enumerate(floors_gens):
        for g in gens:
            initial_gen_pos[type_to_idx[g]] = f
    for f, chips in enumerate(floors_chips):
        for c in chips:
            initial_chip_pos[type_to_idx[c]] = f

    initial_state = (0, tuple(initial_gen_pos), tuple(initial_chip_pos))

    queue = deque([(initial_state, 0)])
    visited = {get_canonical(*initial_state)}

    while queue:
        (e_pos, g_p, c_p), dist = queue.popleft()

        # Victory condition: all items on floor 3 (0-indexed)
        if all(p == 3 for p in g_p) and all(p == 3 for p in c_p):
            return dist

        # Identify items on the current floor
        current_gen_indices = [i for i, p in enumerate(g_p) if p == e_pos]
        current_chip_indices = [i for i, p in enumerate(c_p) if p == e_pos]

        items = [("G", i) for i in current_gen_indices] + [
            ("C", i) for i in current_chip_indices
        ]

        # Possible actions: Move 1 or 2 items
        combinations = list(itertools.combinations(items, 1)) + list(
            itertools.combinations(items, 2)
        )

        for move in combinations:
            # Prefer moving up to moving down
            for direction in [1, -1]:
                next_e = e_pos + direction
                if not (0 <= next_e <= 3):
                    continue

                # Pruning: Don't move items down if all floors below are empty
                if direction == -1:
                    all_below_empty = True
                    for f_idx in range(e_pos):
                        if any(p == f_idx for p in g_p) or any(p == f_idx for p in c_p):
                            all_below_empty = False
                            break
                    if all_below_empty:
                        continue

                new_g_p = list(g_p)
                new_c_p = list(c_p)
                for kind, idx in move:
                    if kind == "G":
                        new_g_p[idx] = next_e
                    else:
                        new_c_p[idx] = next_e

                # Check validity of source and destination floors
                valid = True
                for f_idx in [e_pos, next_e]:
                    f_gens = {i for i, p in enumerate(new_g_p) if p == f_idx}
                    f_chips = {i for i, p in enumerate(new_c_p) if p == f_idx}
                    if not is_valid_floor(f_gens, f_chips):
                        valid = False
                        break

                if valid:
                    next_state = (next_e, tuple(new_g_p), tuple(new_c_p))
                    canonical = get_canonical(*next_state)
                    if canonical not in visited:
                        visited.add(canonical)
                        queue.append((next_state, dist + 1))

    return -1


class TestElevator(unittest.TestCase):
    """
    Unit tests for the elevator puzzle solver.
    """

    def test_example(self) -> None:
        """
        Tests the example provided in the problem description.
        """
        # The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
        # The second floor contains a hydrogen generator.
        # The third floor contains a lithium generator.
        # The fourth floor contains nothing relevant.
        floors_gens = [[], ["hydrogen"], ["lithium"], []]
        floors_chips = [["hydrogen", "lithium"], [], [], []]

        result = solve(floors_gens, floors_chips)
        self.assertEqual(result, 11)


def main() -> None:
    """
    Main entry point for the script.
    """
    # Check for --test flag
    if "--test" in sys.argv:
        sys.argv.remove("--test")
        unittest.main()
        return

    # Use command line argument for input file, or default to input.txt
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "input.txt"

    try:
        floors_gens, floors_chips = parse_input(filename)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    # Part 1
    print("--- Part 1 ---")
    print(f"Loaded from {filename}:")
    print_floors(floors_gens, floors_chips, elevator_floor=0)

    print("\nSolving for minimum actions (Part 1)...")
    result1 = solve(floors_gens, floors_chips)

    if result1 != -1:
        print(f"Part 1: Success! All items moved in {result1} steps.")
    else:
        print("Part 1: Failed to find a solution.")

    # Part 2
    print("\n--- Part 2 ---")
    # Add extra items to floor 1 (index 0)
    # The first floor contains:
    # An elerium generator.
    # An elerium-compatible microchip.
    # A dilithium generator.
    # A dilithium-compatible microchip.
    p2_gens = [list(f) for f in floors_gens]
    p2_chips = [list(f) for f in floors_chips]
    p2_gens[0].extend(["elerium", "dilithium"])
    p2_chips[0].extend(["elerium", "dilithium"])

    print("State for Part 2 (Floor 1 updated):")
    print_floors(p2_gens, p2_chips, elevator_floor=0)

    print("\nSolving for minimum actions (Part 2)...")
    result2 = solve(p2_gens, p2_chips)

    if result2 != -1:
        print(f"Part 2: Success! All items moved in {result2} steps.")
    else:
        print("Part 2: Failed to find a solution.")


if __name__ == "__main__":
    main()
