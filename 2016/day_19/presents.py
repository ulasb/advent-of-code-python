import josephus

# Advent of Code Day 19
# by Ulaş Bardak

NUM_ELVES = 3001330

def solve1(num_elves: int) -> int:
    return josephus.josephus_part1(num_elves)

def solve2(num_elves: int) -> int:
   return josephus.josephus_part2(num_elves)

def main():
    ans1 = solve1(NUM_ELVES)
    print(f"Part 1 Result: {ans1}")

    ans2 = solve2(NUM_ELVES)
    print(f"Part 2 Result: {ans2}")

if __name__ == "__main__":
    main()