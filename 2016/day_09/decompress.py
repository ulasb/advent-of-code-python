"""
Advent of Code 2016 - Day 9: Explosives in Cyberspace
Solution created and published by Ulaş Bardak.
Follows Mozilla Public License 2.0.
"""

import sys


def get_decompressed_length_v1(data: str) -> int:
    """
    Calculate the length of the decompressed data using version 1 rules.

    In version 1, markers are not decompressed - even if the decompressed
    text contains a marker-like sequence, it should be treated as raw text.

    Parameters
    ----------
    data : str
        The compressed string.

    Returns
    -------
    int
        The length of the decompressed string.
    """
    length = 0
    i = 0
    while i < len(data):
        if data[i] == "(":
            end_marker = data.find(")", i)
            marker = data[i + 1 : end_marker]
            l, r = map(int, marker.split("x"))
            i = end_marker + 1
            length += l * r
            i += l
        else:
            length += 1
            i += 1
    return length


def get_decompressed_length_v2(data: str, start: int = 0, end: int | None = None) -> int:
    """
    Calculate the length of the decompressed data using version 2 rules.

    In version 2, markers within decompressed data are also decompressed.
    Operates on indices to avoid excessive string slicing.

    Parameters
    ----------
    data : str
        The compressed string.
    start : int, optional
        Starting index for processing, by default 0.
    end : int, optional
        Ending index for processing, by default None (end of string).

    Returns
    -------
    int
        The length of the decompressed string.
    """
    if end is None:
        end = len(data)

    length = 0
    i = start
    while i < end:
        if data[i] == "(":
            end_marker = data.find(")", i)
            marker = data[i + 1 : end_marker]
            l, r = map(int, marker.split("x"))
            i = end_marker + 1
            # Recursively calculate length of the segment without slicing
            length += get_decompressed_length_v2(data, i, i + l) * r
            i += l
        else:
            length += 1
            i += 1
    return length


def solve(data: str) -> tuple[int, int]:
    """
    Solves both parts of the puzzle for the given input data.

    Parameters
    ----------
    data : str
        The input string.

    Returns
    -------
    tuple[int, int]
        A tuple containing (Part 1 result, Part 2 result).
    """
    return get_decompressed_length_v1(data), get_decompressed_length_v2(data)


def main(filename: str = "input.txt") -> None:
    """
    Main entry point for the decompression script.

    Parameters
    ----------
    filename : str, optional
        Path to the input file, by default "input.txt"
    """
    try:
        with open(filename, "r") as f:
            data = "".join(f.read().split())

        p1, p2 = solve(data)
        print(f"Part 1: {p1}")
        print(f"Part 2: {p2}")

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()
