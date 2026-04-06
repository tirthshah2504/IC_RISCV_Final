#!/usr/bin/env python3

import sys

def convert_hex_to_verilog(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        word = line.strip()
        if word:  # skip empty lines
            print(f"data[{i}] = 32'h{word};")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 hex_to_verilog.py input.hex")
        sys.exit(1)

    convert_hex_to_verilog(sys.argv[1])