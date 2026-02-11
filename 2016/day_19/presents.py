from collections import deque

# Advent of Code Day 19
# by Ulaş Bardak

NUM_ELVES = 3001330

def solve1(num_elves: int) -> int:
    """Solves Part 1 using a simple deque rotation."""
    elves_q = deque(range(1, num_elves + 1))
    
    while len(elves_q) > 1:
        elves_q.rotate(-1)
        elves_q.popleft()        
    return elves_q[0]

def solve2(num_elves: int) -> int:
    """
    Solves Part 2 using two deques to maintain O(1) removals from the 
    opposite side of the circle (O(N) total complexity).
    """
    # Split the elves into two halves
    left = deque(range(1, num_elves // 2 + 1))
    right = deque(range(num_elves // 2 + 1, num_elves + 1))

    while left and right:
        # The elf across is always at the front of 'right' or end of 'left'
        if len(left) > len(right):
            left.pop()
        else:
            right.popleft()

        # Maintenance: Rotate the circle
        if not right: break
        right.append(left.popleft())
        left.append(right.popleft())

    return left[0] if left else right[0]

def main():
    # Example validation for NUM_ELVES = 5 as per AoC instructions
    # Part 1 Sample: 5 elves -> Elf 3 wins
    # Part 2 Sample: 5 elves -> Elf 2 wins
    print("Running Validations...")
    assert(solve1(5) == 3)
    assert(solve2(5) == 2)
    print("Validations passed.\n")

    ans1 = solve1(NUM_ELVES)
    print(f"Part 1 Result: {ans1}")

    ans2 = solve2(NUM_ELVES)
    print(f"Part 2 Result: {ans2}")

if __name__ == "__main__":
    main()