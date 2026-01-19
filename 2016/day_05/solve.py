"""
This module provides the solution for Advent of Code 2016, Day 5.
The logic involves finding MD5 hashes with specific prefixes.

Created and published by Ulaş Bardak.
Following Mozilla Public License 2.0.
MPL 2.0 is a copyleft license that is easy to comply with. It allows you to
distribute the software, but you must make the source code available if you
distribute it in executable form.
"""

import hashlib


def part1(door_id: str) -> str:
    """
    Find the 8-character password using the door ID for Part 1.

    The password is formed by the sixth character of the MD5 hash of
    the door ID followed by an increasing index, provided the hash
    starts with five zeroes.

    Parameters
    ----------
    door_id : str
        The puzzle input door ID.

    Returns
    -------
    str
        The 8-character password.
    """
    password = ""
    index = 0
    base_hasher = hashlib.md5(door_id.encode())

    while len(password) < 8:
        # Optimization: use digest bytes to avoid hex string conversion in hot loop
        m = base_hasher.copy()
        m.update(str(index).encode())
        digest = m.digest()

        # Check if hash starts with five zeroes in hex (00 00 0x)
        if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
            # The 6th character is the low nibble of the 3rd byte
            password += f"{digest[2]:x}"
        index += 1
    return password


def part2(door_id: str) -> str:
    """
    Find the 8-character password using the door ID for Part 2.

    The password is formed by placing the seventh character of the hash at
    the position specified by the sixth character, provided the hash
    starts with five zeroes and the position is valid (0-7).

    Parameters
    ----------
    door_id : str
        The puzzle input door ID.

    Returns
    -------
    str
        The 8-character password.
    """
    password = ["_"] * 8
    found_count = 0
    index = 0
    base_hasher = hashlib.md5(door_id.encode())

    while found_count < 8:
        m = base_hasher.copy()
        m.update(str(index).encode())
        digest = m.digest()

        # Check if hash starts with five zeroes in hex (00 00 0x)
        if digest[0] == 0 and digest[1] == 0 and digest[2] < 16:
            pos = digest[2]
            # Valid positions are 0-7, and we only fill if not already filled
            if pos < 8 and password[pos] == "_":
                # The 7th character is the high nibble of the 4th byte
                char = f"{digest[3] >> 4:x}"
                password[pos] = char
                found_count += 1
        index += 1
    return "".join(password)


def main(file_path: str = "input.txt") -> None:
    """
    Main entry point for the script. Reads the input and prints the solutions.

    Parameters
    ----------
    file_path : str, optional
        Path to the input file, by default "input.txt"
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            door_id = f.read().strip()
    except FileNotFoundError:
        # Default door_id if file not found, as per common AoC structure
        door_id = "cxdnnyjw"

    print(f"Part 1: {part1(door_id)}")
    print(f"Part 2: {part2(door_id)}")


if __name__ == "__main__":
    main()
