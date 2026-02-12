# Advent of Code 2016 Day 20
# by Ulaş Bardak

def parse_ranges(filename):
    """Parses IP ranges from the input file."""
    with open(filename, "r") as f:
        return [tuple(map(int, line.strip().split("-"))) for line in f.readlines()]

def merge_ranges(ranges):
    """Merges overlapping and adjacent IP ranges. Does not modify the input list."""
    if not ranges:
        return []

    # Sort a copy of the ranges by the first number
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]
    for r in sorted_ranges[1:]:
        last_range = merged[-1]
        if r[0] <= last_range[1] + 1:
            merged[-1] = (last_range[0], max(last_range[1], r[1]))
        else:
            merged.append(r)
    return merged

def solve_part1(merged_ranges):
    """Finds the first IP that is not in any of the ranges."""
    first_allowed_ip = 0
    for start, end in merged_ranges:
        if first_allowed_ip < start:
            break
        first_allowed_ip = end + 1
    return first_allowed_ip

def solve_part2(merged_ranges, max_ip):
    """Counts the number of allowed IPs."""
    blocked_count = sum(end - start + 1 for start, end in merged_ranges)
    return max_ip - blocked_count + 1

def main():
    """Main function to solve the puzzle."""
    INPUT_FILE = "input.txt"
    MAX_IP = 4294967295

    ranges = parse_ranges(INPUT_FILE)
    merged = merge_ranges(ranges)

    part1_solution = solve_part1(merged)
    print(f"Part 1: {part1_solution}")

    part2_solution = solve_part2(merged, MAX_IP)
    print(f"Part 2: {part2_solution}")

if __name__ == "__main__":
    main()