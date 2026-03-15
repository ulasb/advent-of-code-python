"""
Solution for Advent of Code 2017, Day 7: Recursive Circus.
Created by Ulaş Bardak.
This code is published under the Mozilla Public License 2.0.
"""

from typing import Dict, List


class Program:
    """Represents a program in the tower."""

    def __init__(self, name: str, weight: int, children: List[str]):
        """
        Initializes a new Program instance.

        Parameters
        ----------
        name : str
            The name of the program.
        weight : int
            The weight of the program.
        children : List[str]
            A list of child program names.
        """
        self.name = name
        self.weight = weight
        self.children = children
        self.total_weight = 0


def parse_input(filepath: str) -> Dict[str, Program]:
    """
    Parses the input file to create a dictionary of Programs.

    Parameters
    ----------
    filepath : str
        The path to the input file.

    Returns
    -------
    Dict[str, Program]
        A mapping from program name to the Program object.
    """
    programs = {}
    with open(filepath, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split(" -> ")
            name_weight = parts[0].split()
            name = name_weight[0]
            weight = int(name_weight[1].strip("()"))

            children = []
            if len(parts) > 1:
                children = [child.strip() for child in parts[1].split(",")]

            programs[name] = Program(name, weight, children)

    return programs


def find_bottom_program(programs: Dict[str, Program]) -> str:
    """
    Finds the name of the bottom program (Part 1).

    Parameters
    ----------
    programs : Dict[str, Program]
        A dictionary of all programs.

    Returns
    -------
    str
        The name of the bottom program.
    """
    all_children = set()
    for program in programs.values():
        all_children.update(program.children)

    for name in programs.keys():
        if name not in all_children:
            return name

    raise ValueError("No bottom program found")


def calculate_weights(programs: Dict[str, Program], root: str) -> int:
    """
    Recursively calculates and sets the total weight of each program's tower.

    Parameters
    ----------
    programs : Dict[str, Program]
        A dictionary of all programs.
    root : str
        The name of the root program to start calculation.

    Returns
    -------
    int
        The total weight of the root program's tower.
    """
    program = programs[root]
    total_weight = program.weight

    for child in program.children:
        total_weight += calculate_weights(programs, child)

    program.total_weight = total_weight
    return total_weight


def find_imbalance(programs: Dict[str, Program], node: str, target_weight: int) -> int:
    """
    Finds the corrected weight of the program causing the imbalance (Part 2).

    Parameters
    ----------
    programs : Dict[str, Program]
        A dictionary of all programs.
    node : str
        The current program name being checked.
    target_weight : int
        The expected total weight this node should have.

    Returns
    -------
    int
        The corrected weight of the imbalanced program.
    """
    program = programs[node]

    if not program.children:
        # If no children, the imbalance must be this node itself
        diff = program.total_weight - target_weight
        return program.weight - diff

    child_weights = {}
    for child in program.children:
        weight = programs[child].total_weight
        if weight not in child_weights:
            child_weights[weight] = []
        child_weights[weight].append(child)

    if len(child_weights) == 1:
        # All children are balanced, so the imbalance is exactly at this node
        diff = program.total_weight - target_weight
        return program.weight - diff

    # There is an imbalance among the children
    abnormal_weight = None
    normal_weight = None
    abnormal_node = None
    for weight, children_list in child_weights.items():
        if len(children_list) == 1:
            abnormal_weight = weight
            abnormal_node = children_list[0]
        else:
            normal_weight = weight

    if abnormal_node is None or normal_weight is None:
        # This shouldn't happen based on the problem description
        raise ValueError("Could not find the distinct unbalanced child.")

    # The abnormal node is the one causing the imbalance, drill down into it
    return find_imbalance(programs, abnormal_node, normal_weight)


def solve_part_1(filepath: str = "input.txt") -> str:
    """
    Solves Part 1 of the day's challenge.

    Parameters
    ----------
    filepath : str
        The path to the input file.

    Returns
    -------
    str
        The name of the bottom program.
    """
    programs = parse_input(filepath)
    return find_bottom_program(programs)


def solve_part_2(filepath: str = "input.txt") -> int:
    """
    Solves Part 2 of the day's challenge.

    Parameters
    ----------
    filepath : str
        The path to the input file.

    Returns
    -------
    int
        The corrected weight of the imbalanced program.
    """
    programs = parse_input(filepath)
    root = find_bottom_program(programs)

    # Calculate all total weights
    calculate_weights(programs, root)

    program = programs[root]

    child_weights = {}
    for child in program.children:
        weight = programs[child].total_weight
        if weight not in child_weights:
            child_weights[weight] = []
        child_weights[weight].append(child)

    if len(child_weights) <= 1:
        raise ValueError("The tower is completely balanced.")

    abnormal_weight = None
    normal_weight = None
    abnormal_node = None
    for weight, children_list in child_weights.items():
        if len(children_list) == 1:
            abnormal_weight = weight
            abnormal_node = children_list[0]
        else:
            normal_weight = weight

    if abnormal_node is None or normal_weight is None:
        raise ValueError("Could not find the distinct unbalanced child from root.")

    return find_imbalance(programs, abnormal_node, normal_weight)


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
    print(f"Part 2: {solve_part_2()}")
