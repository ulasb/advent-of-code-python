# SPDX-License-Identifier: MPL-2.0
# Code created and published by Ulaş Bardak
# This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.
# If a copy of the MPL was not distributed with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

import unittest
import sys
from typing import Callable, Dict, Any


def swap_x_y(password: str, x: int, y: int) -> str:
    """Swap characters at positions x and y.

    Parameters
    ----------
    password : str
        The password string to modify.
    x : int
        First position index.
    y : int
        Second position index.

    Returns
    -------
    str
        Password with characters at positions x and y swapped.
    """
    password_list = list(password)
    password_list[x], password_list[y] = password_list[y], password_list[x]
    return "".join(password_list)


def swap_letter_x_y(password: str, x: str, y: str) -> str:
    """Swap all occurrences of characters x and y in the password.

    Parameters
    ----------
    password : str
        The password string to modify.
    x : str
        First character to swap.
    y : str
        Second character to swap.

    Returns
    -------
    str
        Password with characters x and y swapped.
    """
    password_list = list(password)
    for i in range(len(password_list)):
        if password_list[i] == x:
            password_list[i] = y
        elif password_list[i] == y:
            password_list[i] = x
    return "".join(password_list)


def rotate_left_right_x_steps(password: str, direction: str, steps: int) -> str:
    """Rotate password left or right by a given number of steps.

    Parameters
    ----------
    password : str
        The password string to rotate.
    direction : str
        Direction of rotation: 'left' or 'right'.
    steps : int
        Number of positions to rotate.

    Returns
    -------
    str
        Rotated password.
    """
    steps = steps % len(password)
    if direction == "left":
        return password[steps:] + password[:steps]
    else:
        return password[-steps:] + password[:-steps]


def rotate_based_on_position(password: str, letter: str) -> str:
    """Rotate password based on the position of a letter.

    Rotates right by 1 + index + (1 if index >= 4, else 0), where
    index is the position of the letter.

    Parameters
    ----------
    password : str
        The password string to rotate.
    letter : str
        The letter to find the position of.

    Returns
    -------
    str
        Rotated password.
    """
    index = password.index(letter)
    steps = 1 + index + (1 if index >= 4 else 0)
    return rotate_left_right_x_steps(password, "right", steps)


def reverse_positions_x_through_y(password: str, x: int, y: int) -> str:
    """Reverse the substring from position x to y (inclusive).

    Parameters
    ----------
    password : str
        The password string to modify.
    x : int
        Start position of the substring.
    y : int
        End position of the substring.

    Returns
    -------
    str
        Password with substring reversed.
    """
    password_list = list(password)
    password_list[x : y + 1] = password_list[x : y + 1][::-1]
    return "".join(password_list)


def move_position_x_to_position_y(password: str, x: int, y: int) -> str:
    """Move character at position x to position y.

    Parameters
    ----------
    password : str
        The password string to modify.
    x : int
        Current position of the character.
    y : int
        Target position for the character.

    Returns
    -------
    str
        Password with character moved.
    """
    password_list = list(password)
    char = password_list.pop(x)
    password_list.insert(y, char)
    return "".join(password_list)


def parse_command(transformation: str) -> tuple[str, Dict[str, Any]]:
    """Parse a command string into command type and parameters.

    Parameters
    ----------
    transformation : str
        The transformation command string.

    Returns
    -------
    tuple[str, Dict[str, Any]]
        A tuple of (command_type, parameters_dict).
    """
    parts = transformation.split()

    if transformation.startswith("swap position"):
        return ("swap_position", {"x": int(parts[2]), "y": int(parts[5])})
    elif transformation.startswith("swap letter"):
        return ("swap_letter", {"x": parts[2], "y": parts[5]})
    elif transformation.startswith("rotate left"):
        return ("rotate_left", {"steps": int(parts[2])})
    elif transformation.startswith("rotate right"):
        return ("rotate_right", {"steps": int(parts[2])})
    elif transformation.startswith("rotate based"):
        return ("rotate_based", {"letter": parts[6]})
    elif transformation.startswith("reverse positions"):
        return ("reverse", {"x": int(parts[2]), "y": int(parts[4])})
    elif transformation.startswith("move position"):
        return ("move", {"x": int(parts[2]), "y": int(parts[5])})
    else:
        raise ValueError(f"Unknown transformation: {transformation}")


def apply_transformations(
    password: str, transformations: list[str], reverse: bool = False
) -> str:
    """Apply transformations (forward or reverse) to a password.

    Parameters
    ----------
    password : str
        The initial password.
    transformations : list[str]
        List of transformation commands.
    reverse : bool, optional
        If True, apply reverse transformations. Default is False.

    Returns
    -------
    str
        The transformed password.
    """
    # Forward dispatch table
    forward_ops: Dict[str, Callable] = {
        "swap_position": lambda pw, x, y: swap_x_y(pw, x, y),
        "swap_letter": lambda pw, x, y: swap_letter_x_y(pw, x, y),
        "rotate_left": lambda pw, steps: rotate_left_right_x_steps(pw, "left", steps),
        "rotate_right": lambda pw, steps: rotate_left_right_x_steps(pw, "right", steps),
        "rotate_based": lambda pw, letter: rotate_based_on_position(pw, letter),
        "reverse": lambda pw, x, y: reverse_positions_x_through_y(pw, x, y),
        "move": lambda pw, x, y: move_position_x_to_position_y(pw, x, y),
    }

    # Reverse dispatch table (operations to undo)
    reverse_ops: Dict[str, Callable] = {
        "swap_position": lambda pw, x, y: swap_x_y(pw, y, x),
        "swap_letter": lambda pw, x, y: swap_letter_x_y(pw, y, x),
        "rotate_left": lambda pw, steps: rotate_left_right_x_steps(pw, "right", steps),
        "rotate_right": lambda pw, steps: rotate_left_right_x_steps(pw, "left", steps),
        "rotate_based": lambda pw, letter: _undo_rotate_based(pw, letter),
        "reverse": lambda pw, x, y: reverse_positions_x_through_y(pw, x, y),
        "move": lambda pw, x, y: move_position_x_to_position_y(pw, y, x),
    }

    ops = reverse_ops if reverse else forward_ops
    trans_list = transformations[::-1] if reverse else transformations

    for transformation in trans_list:
        cmd_type, params = parse_command(transformation)
        op = ops[cmd_type]

        password = op(password, **params)

    return password


def _undo_rotate_based(password: str, letter: str) -> str:
    """Undo a rotate-based-on-position operation.

    Tries all possible rotations to find the one that produces the current
    password when the forward rotation is applied.

    Parameters
    ----------
    password : str
        The current (rotated) password.
    letter : str
        The letter used in the original rotation.

    Returns
    -------
    str
        The password before the rotation.
    """
    for i in range(len(password)):
        candidate = rotate_left_right_x_steps(password, "left", i)
        if rotate_based_on_position(candidate, letter) == password:
            return candidate
    raise ValueError(f"Could not find reverse rotation for letter '{letter}'")


def main(input_file: str) -> None:
    """Solve both parts of the puzzle.

    Part 1: Apply transformations to initial password 'abcdefgh'.
    Part 2: Reverse transformations on scrambled password 'fbgdceah'.

    Parameters
    ----------
    input_file : str
        Path to the input file containing transformation commands.
    """
    with open(input_file, "r") as f:
        transformations = [line for line in f.read().splitlines() if line.strip()]

    # Part 1: Scramble password
    initial_password = "abcdefgh"
    final_password = apply_transformations(initial_password, transformations)
    print(f"Part 1: Scrambled password - {final_password}")

    # Part 2: Unscramble password
    scrambled_password = "fbgdceah"
    unscrambled_password = apply_transformations(
        scrambled_password, transformations, reverse=True
    )
    print(f"Part 2: Unscrambled password - {unscrambled_password}")


class TestFundamentals(unittest.TestCase):
    """Unit tests for password transformation functions."""

    def test_swap_x_y(self) -> None:
        """Test swapping positions."""
        self.assertEqual(swap_x_y("abcde", 4, 0), "ebcda")

    def test_swap_letter_x_y(self) -> None:
        """Test swapping letters."""
        self.assertEqual(swap_letter_x_y("ebcda", "d", "b"), "edcba")

    def test_rotate_left_right_x_steps(self) -> None:
        """Test left and right rotations."""
        self.assertEqual(rotate_left_right_x_steps("edcba", "left", 1), "dcbae")
        self.assertEqual(rotate_left_right_x_steps("dcbae", "right", 1), "edcba")

    def test_rotate_based_on_position(self) -> None:
        """Test rotation based on letter position."""
        self.assertEqual(rotate_based_on_position("abdec", "b"), "ecabd")

    def test_reverse_positions_x_through_y(self) -> None:
        """Test reversing a substring."""
        self.assertEqual(reverse_positions_x_through_y("edcba", 0, 4), "abcde")

    def test_move_position_x_to_position_y(self) -> None:
        """Test moving a character to a new position."""
        self.assertEqual(move_position_x_to_position_y("bcdea", 1, 4), "bdeac")


if __name__ == "__main__":
    # Get arguments: optionally "test" to run unit tests or "input_file" with path
    input_file = "input.txt"
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            unittest.main(argv=[""], exit=False)
        elif sys.argv[1] == "input_file" and len(sys.argv) > 2:
            input_file = sys.argv[2]
    main(input_file)