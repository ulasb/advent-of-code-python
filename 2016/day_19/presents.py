NUM_ELVES = 3001330
#NUM_ELVES = 5

class Elf:
    def __init__(self, id):
        self.id = id
        self.presents = 1

    def __repr__(self):
        return f"Elf {self.id} with {self.presents} presents"

def solve1(elves: list[Elf]) -> int:
    to_be_removed_idx = -1  
    starting_point = 0
    while len(elves) > 1:
        if(len(elves) % 1000 == 0):
            print(len(elves))
        for i in range(starting_point,len(elves)):
            # Go through each elf and steal presents from the next elf
            if i == len(elves) - 1:
                # elves[i].presents += elves[0].presents
                to_be_removed_idx = 0
                starting_point = 0
            else:
                # elves[i].presents += elves[i + 1].presents
                to_be_removed_idx = i + 1
                starting_point = i + 1
            break
        elves.pop(to_be_removed_idx)
    print(elves[0])
    exit()  

elves = [Elf(i) for i in range(1, NUM_ELVES + 1)]
solve1(elves)