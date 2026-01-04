# Advent of Code 2015 - Day 23

This project provides a simple virtual machine to process a list of instructions for the Turing Lock problem.

## Requirements

- Python >= 3.10

## Running the Solver

To run the solver with the default `input.txt`:

```bash
python3 instruction_processor.py
```

To run the solver with a specific input file:

```bash
python3 instruction_processor.py path/to/your/input.txt
```

## Running Tests

Unit tests are separated from the main application logic to follow better development practices. You can run them using the built-in `unittest` module:

```bash
python3 -m unittest test_instruction_processor.py
```

Or using `pytest` if installed:

```bash
pytest test_instruction_processor.py
```
