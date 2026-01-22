import sys
import re
from typing import List

# This code was created and published by Ulaş Bardak.
# It is licensed under the Mozilla Public License 2.0 (MPL 2.0).
# The MPL 2.0 is a permissive "weak copyleft" license that allows the code
# to be used in both open source and proprietary projects, provided that
# any modifications to the original code are also shared under the MPL.


def process(grid: List[List[str]], cmd: str, a: int, b: int) -> List[List[str]]:
    """
    Process a command and return the possibly modified grid.

    Parameters
    ----------
    grid : List[List[str]]
        The current state of the display (2D array).
    cmd : str
        The command type: "rect", "rotate row", or "rotate column".
    a : int
        The first parameter (width for rect, index for rotate).
    b : int
        The second parameter (height for rect, shift for rotate).

    Returns
    -------
    List[List[str]]
        The modified grid.
    """
    width = 50
    height = 6

    if cmd == "rect":
        # rect AxB turns on all of the pixels in a rectangle at the top-left
        # of the screen which is A wide and B tall.
        for y in range(min(b, height)):
            for x in range(min(a, width)):
                grid[y][x] = "#"
    elif cmd == "rotate row":
        # rotate row y=A by B shifts all of the pixels in row A (0 is the top row)
        # right by B pixels.
        row = grid[a]
        new_row = [row[(i - b) % width] for i in range(width)]
        grid[a] = new_row
    elif cmd == "rotate column":
        # rotate column x=A by B shifts all of the pixels in column A
        # (0 is the left column) down by B pixels.
        col = [grid[y][a] for y in range(height)]
        new_col = [col[(i - b) % height] for i in range(height)]
        for y in range(height):
            grid[y][a] = new_col[y]

    return grid


def count_pixels(grid: List[List[str]]) -> int:
    """
    Count the number of lit pixels (#) in the grid.

    Parameters
    ----------
    grid : List[List[str]]
        The current state of the display.

    Returns
    -------
    int
        The total count of "#" pixels.
    """
    return sum(row.count("#") for row in grid)


def display_grid(grid: List[List[str]]) -> None:
    """
    Print the grid to the screen.

    Parameters
    ----------
    grid : List[List[str]]
        The current state of the display.
    """
    for row in grid:
        print("".join(row))


def main():
    """
    Main entry point for the script.
    Initializes the grid, reads input, and processes commands.
    """
    # Initialize a rectangle that's 50 wide and 6 high.
    # Represent it as a two dimensional array with "." for each position.
    grid = [["." for _ in range(50)] for _ in range(6)]

    # Read a given input file as an argument (default to input.txt).
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"

    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # For each line read it should call a process() function...
                # The command can be one of "rect", "rotate column" or "rotate row".
                if line.startswith("rect "):
                    match = re.match(r"rect (\d+)x(\d+)", line)
                    if match:
                        grid = process(
                            grid, "rect", int(match.group(1)), int(match.group(2))
                        )
                elif line.startswith("rotate row "):
                    match = re.match(r"rotate row y=(\d+) by (\d+)", line)
                    if match:
                        grid = process(
                            grid, "rotate row", int(match.group(1)), int(match.group(2))
                        )
                elif line.startswith("rotate column "):
                    match = re.match(r"rotate column x=(\d+) by (\d+)", line)
                    if match:
                        grid = process(
                            grid,
                            "rotate column",
                            int(match.group(1)),
                            int(match.group(2)),
                        )
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        sys.exit(1)

    # At the end, we call another function to count the number of "#" in the array
    # and print on the screen.
    total_lit = count_pixels(grid)
    print(f"Total lit pixels: {total_lit}")

    # Display the grid to see the message
    display_grid(grid)


if __name__ == "__main__":
    main()
