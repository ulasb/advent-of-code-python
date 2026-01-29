"""
Advent of Code 2016 - Day 12
Leonardo's Monorail

This code was created and published by Ulaş Bardak.
License: Mozilla Public License 2.0
The Mozilla Public License 2.0 is a free and open-source software license
that allows for the use, modification, and distribution of the software,
provided that any modifications to the licensed code are also made available
under the same license.
"""

import sys
from typing import Dict, List


def run_program(
    instructions: List[str], initial_registers: Dict[str, int]
) -> Dict[str, int]:
    """
    Executes the assembly program with the given instructions and initial registers.

    Parameters
    ----------
    instructions : List[str]
        A list of instruction strings.
    initial_registers : Dict[str, int]
        A dictionary containing the initial values of registers 'a', 'b', 'c', and 'd'.

    Returns
    -------
    Dict[str, int]
        The final state of the registers after the program halts.
    """
    # Map registers to indices
    reg_map = {"a": 0, "b": 1, "c": 2, "d": 3}
    regs = [0] * 4
    for r, v in initial_registers.items():
        regs[reg_map[r]] = v

    # Pre-parse instructions
    CPY, INC, DEC, JNZ = 0, 1, 2, 3
    op_map = {"cpy": CPY, "inc": INC, "dec": DEC, "jnz": JNZ}

    parsed_instrs = []
    for line in instructions:
        parts = line.split()
        cmd = op_map[parts[0]]
        args = []
        for p in parts[1:]:
            if p in reg_map:
                args.append((True, reg_map[p]))
            else:
                args.append((False, int(p)))
        parsed_instrs.append((cmd, args))

    pc = 0
    n = len(parsed_instrs)

    while pc < n:
        cmd, args = parsed_instrs[pc]

        # Simple Peephole Optimization: Addition Loop
        if pc + 2 < n:
            cmd2, args2 = parsed_instrs[pc + 1]
            cmd3, args3 = parsed_instrs[pc + 2]
            if (
                cmd3 == JNZ
                and args3[0] == (True, args2[0][1])
                and args3[1] == (False, -2)
            ):
                if cmd == INC and cmd2 == DEC:
                    reg_a = args[0][1]
                    reg_b = args2[0][1]
                    regs[reg_a] += regs[reg_b]
                    regs[reg_b] = 0
                    pc += 3
                    continue
                elif cmd == DEC and cmd2 == INC:
                    reg_a = args2[0][1]
                    reg_b = args[0][1]
                    regs[reg_a] += regs[reg_b]
                    regs[reg_b] = 0
                    pc += 3
                    continue

        if cmd == CPY:
            is_reg, val = args[0]
            regs[args[1][1]] = regs[val] if is_reg else val
            pc += 1
        elif cmd == INC:
            regs[args[0][1]] += 1
            pc += 1
        elif cmd == DEC:
            regs[args[0][1]] -= 1
            pc += 1
        elif cmd == JNZ:
            is_reg, val = args[0]
            val = regs[val] if is_reg else val
            if val != 0:
                pc += args[1][1]
            else:
                pc += 1
        else:
            pc += 1

    # Convert back to dictionary
    return {r: regs[i] for r, i in reg_map.items()}


def main() -> None:
    """
    Main function to read input and run the program.
    """
    filename = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            instructions = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return

    # Initialize registers a, b, c, d to 0
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    final_registers = run_program(instructions, registers)
    print("[Part 1] Value of register a: ", final_registers["a"])

    # Initialize registers a, b, c, d to 0
    registers = {"a": 0, "b": 0, "c": 1, "d": 0}
    final_registers = run_program(instructions, registers)
    print("[Part 2] Value of register a: ", final_registers["a"])


if __name__ == "__main__":
    main()
