# Advent of Code 2016 Day 20
# by Ulaş Bardak

INPUT_FILE = "input.txt"
MAX_IP = 4294967295

with open(INPUT_FILE, "r") as f:
    ranges = [tuple(map(int, line.strip().split("-"))) for line in f.readlines()]

# We have the list of ranges, we need to find the first number that is not in any of the ranges.
# The ranges are inclusive.

# Sort the ranges by the first number
ranges.sort()

# Merge overlapping ranges
merged_ranges = []
for r in ranges:
    if not merged_ranges:
        merged_ranges.append(r)
    else:
        last_range = merged_ranges[-1]
        if r[0] <= last_range[1] + 1:
            merged_ranges[-1] = (last_range[0], max(last_range[1], r[1]))
        else:
            merged_ranges.append(r)

# Part 1
# Find the first number that is not in any of the ranges
first_number = 0
for r in merged_ranges:
    if first_number < r[0]:
        break
    first_number = r[1] + 1

print("Part 1: ", first_number)

# Part 2
# Count the number of integers in the range [0, MAX_IP] that are not in any of the ranges
count = 0
for r in merged_ranges:
    count += r[1] - r[0] + 1

print("Part 2: ", MAX_IP - count + 1)
