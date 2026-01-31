import hashlib
import re
from collections import deque, Counter
import multiprocessing

# Advent of Code 2016 - Day 14: One-Time Pad
# Highly optimized version with sliding window and parallel processing support.

SALT = "ihaygndm"
STRETCH = False  # Set to True for Part 2 (key stretching)
NUM_KEYS = 64

def get_hash_stretched(salt_index_tuple):
    """
    Worker function for parallel hashing.
    """
    salt, index, stretched = salt_index_tuple
    h = hashlib.md5((salt + str(index)).encode()).hexdigest()
    if stretched:
        for _ in range(2016):
            h = hashlib.md5(h.encode()).hexdigest()
    return h

class HashProvider:
    """
    Provides hashes for indices, pre-calculating them in chunks
    using multiple cores for maximum performance.
    """
    def __init__(self, salt, stretched, chunk_size=5000):
        self.salt = salt
        self.stretched = stretched
        self.chunk_size = chunk_size
        self.cache = {}
        self.next_index = 0
        self.pool = multiprocessing.Pool()

    def _precompute_next_chunk(self):
        start = self.next_index
        end = start + self.chunk_size
        
        # Prepare arguments for the pool
        args = [(self.salt, i, self.stretched) for i in range(start, end)]
        
        # Compute hashes in parallel
        results = self.pool.map(get_hash_stretched, args)
        
        for i, h in enumerate(results):
            self.cache[start + i] = h
            
        self.next_index = end

    def get(self, index):
        while index not in self.cache:
            self._precompute_next_chunk()
        return self.cache[index]

def find_all_quintets(h):
    """Returns a set of all characters that appear 5 times in a row."""
    # Matches any character (.) followed by itself 4 more times
    return set(re.findall(r'(.)\1{4}', h))

def solve():
    print(f"--- Advent of Code 2016 Day 14 ---")
    print(f"Salt: {SALT}")
    print(f"Mode: {'Part 2 (Stretched)' if STRETCH else 'Part 1 (Normal)'}")
    
    # Initialize Hash Provider
    # If STRETCH is False, we use small chunks as it's very fast anyway.
    # If STRETCH is True, larger chunks help mitigate pool overhead.
    chunk_size = 5000 if STRETCH else 1000
    hasher = HashProvider(SALT, STRETCH, chunk_size=chunk_size)
    
    hashes = deque()
    quintet_counts = Counter()
    triplet_re = re.compile(r'(.)\1{2}')
    
    print("Initializing lookahead window (1000 hashes)...")
    for i in range(1001):
        h = hasher.get(i)
        hashes.append(h)
        if i > 0:
            for char in find_all_quintets(h):
                quintet_counts[char] += 1
    
    keys = []
    index = 0
    
    print(f"Searching for {NUM_KEYS} keys...")
    while len(keys) < NUM_KEYS:
        current_hash = hashes[0]
        
        # Check for first triplet
        match = triplet_re.search(current_hash)
        if match:
            char = match.group(1)
            # Check if this character has a quintet in the next 1000 hashes
            if quintet_counts[char] > 0:
                keys.append(index)
                print(f"  [{len(keys):2}/{NUM_KEYS}] Found key at index {index:6}")
        
        # Move sliding window:
        # 1. The hash at hashes[1] is about to become the current hash.
        #    Its quintets should be removed from the lookahead count.
        next_to_be_current = hashes[1]
        for char in find_all_quintets(next_to_be_current):
            quintet_counts[char] -= 1
            
        # 2. Pop current hash
        hashes.popleft()
        
        # 3. Fetch index + 1001 and add to windows
        index += 1
        new_h = hasher.get(index + 1000)
        hashes.append(new_h)
        for char in find_all_quintets(new_h):
            quintet_counts[char] += 1

    print("-" * 35)
    print(f"SUCCESS! The {NUM_KEYS}th key is at index: {keys[63]}")

if __name__ == "__main__":
    solve()
