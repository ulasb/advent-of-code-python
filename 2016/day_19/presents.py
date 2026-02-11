from collections import deque

NUM_ELVES = 3001330
#NUM_ELVES = 5

class Elf:
    def __init__(self, id):
        self.id = id
        self.presents = 1

    def __repr__(self):
        return f"Elf {self.id} with {self.presents} presents"

def solve1(elves: list[Elf]) -> int:
    elves_q = deque(elves)
    
    while len(elves_q) > 1:
        elves_q.rotate(-1)
        elves_q.popleft()        
    return elves_q[0].id

def solve2(elves: list[Elf]) -> int:
    elves_q = deque(elves)
    
    while len(elves_q) > 1:
        elves_q.rotate(len(elves_q)//2)
        elves_q.popleft()        
    return elves_q[0].id

elves = [Elf(i) for i in range(1, NUM_ELVES + 1)]
print("ID of the elf with all the presents: ", solve1(elves))
print("ID of the elf with all the presents: ", solve2(elves))