# Advent of Code 2016 - Day 14: One-Time Pad

This project provides a highly optimized solution to [Advent of Code 2016 Day 14](https://adventofcode.com/2016/day/14). The task involves generating "One-Time Pad" keys by searching for specific patterns in MD5 hashes.

## The Challenge

To generate a key, you must find an index $i$ such that:
1.  The MD5 hash of `salt + index` contains a **triplet** (three of the same character in a row, e.g., `777`). Only the **first** triplet in the hash is considered.
2.  One of the **next 1000 hashes** (indices $i+1$ to $i+1000$) contains a **quintet** (five in a row) of that same character (e.g., `77777`).

In Part 2, "Key Stretching" is introduced, where each hash is re-hashed 2016 additional times (2017 total iterations), making the computation significantly more intensive.

## Algorithm & Optimizations

The naive approach of checking 1000 ahead for every triplet found leads to an $O(N \times 1000)$ complexity. This implementation uses several advanced techniques to achieve near-optimal performance:

### 1. Sliding Window with Quintet Counter
Instead of scanning 1000 hashes forward every time a triplet is found, we maintain a **sliding window** of 1001 hashes:
-   **Leading Edge**: As indices enter the window at position +1000, we scan them once for all possible quintets and increment a `Counter` for those characters.
-   **Trailing Edge**: As the current index moves past, we remove its quintet contributions from the `Counter`.
-   **Verification**: Checking if a triplet character has a corresponding quintet in the next 1000 indices becomes a **constant time $O(1)$** dictionary lookup.

This reduces the algorithmic complexity from $O(N \times 1000)$ to a linear **$O(N)$**.

### 2. Parallel Hash Generation (Multiprocessing)
Key stretching (Part 2) is the primary bottleneck. Even with algorithmic optimizations, computing 2017 MD5 iterations per index is CPU-heavy. 
-   We utilize a `multiprocessing.Pool` to distribute hash generation across all available CPU cores.
-   Hashes are pre-computed in configurable **chunks**, reducing the overhead of process communication.

### 3. Resource Safety & Design
-   **Context Manager**: The `HashProvider` class implements `__enter__` and `__exit__`, ensuring that the worker pool is gracefully closed and joined, preventing zombie processes or memory leaks.
-   **Lazy Evaluation**: The provider only computes hashes as needed, but does so in parallel chunks to keep the pipeline full.
-   **Parameter Injection**: The `solve` function is decoupled from global state, allowing for easy testing with different salts or key counts.

## Usage

### Configuration
Edit the constants at the top of `pad.py`:
-   `SALT`: Your puzzle input (default: `ihaygndm`).
-   `STRETCH`: Set to `False` for Part 1, `True` for Part 2.
-   `NUM_KEYS`: Number of keys to find (default: `64`).

### Execution
Run the script using Python 3:
```bash
python3 pad.py
```

## Performance
-   **Part 1**: Near instantaneous (< 1s).
-   **Part 2**: Typically completes in ~20-40 seconds on modern multi-core systems (depending on core count), compared to several minutes for a single-threaded implementation.
