# RV32I Bare-Metal Flow using riscv64 Toolchain

This document explains the complete workflow to:
1. Install the RISC-V GNU toolchain  
2. Build and run a RV32I program compatible with our riscv core 


---

## 1. Install GNU Toolchain

We use the `gcc-riscv64-unknown-elf` toolchain. Even though it is a 64-bit toolchain, it supports generating **RV32I** code.

### Install (Ubuntu / WSL)

```bash
sudo apt update
sudo apt install gcc-riscv64-unknown-elf
```

### Verify
```bash
riscv64-unknown-elf-gcc --version
```

---

## 2. How to Build and Run

Make the build script executable:
```bash
chmod +x build.sh
```

Run:
```bash
./build.sh
```

**This produces:**
* `program.elf` → linked ELF file
* `program.bin` → raw binary
* `program.hex` → word-aligned hex
* Verilog-formatted output to be pasted in Instruction_Memory.v

---

## 3. build.sh Explanation

```bash
set -e  # stop on first error

riscv64-unknown-elf-gcc \
  -march=rv32i \
  -mabi=ilp32 \
  -nostdlib \
  -ffreestanding \
  -Wl,-T,link.ld \
  start.S main.c \
  -o program.elf

riscv64-unknown-elf-objcopy -O binary program.elf program.bin

hexdump -v -e '1/4 "%08x\n"' program.bin > program.hex

# Print to terminal
python3 hex_to_verilog.py program.hex
```

### What each step does:

**Compilation + Linking**
* Compiles `start.S` and `main.c`
* Links using `link.ld`
* Targets:
  * `-march=rv32i` → base RV32I ISA
  * `-mabi=ilp32` → 32-bit ABI
  * `-nostdlib` → no standard libraries
  * `-ffreestanding` → bare-metal environment

**Binary Generation**
* `objcopy` converts ELF → raw binary

**Hex Conversion**
* `hexdump` formats binary into 32-bit words (one per line)

**Verilog Conversion**
* Python script converts hex → Verilog memory initialization format

---

## 4. hex_to_verilog.py Explanation

```python
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
```

### Purpose:
* Reads `program.hex`
* Converts each 32-bit word into: `data[index] = 32'hXXXXXXXX;`
* Used for initializing instruction memory in Instruction_Memory.v

---

## 5. start.S (Program Entry)

```assembly
.section .text
.globl _start

_start:
    call main
1:  j 1b
```

### Explanation:
* `_start` is the entry point
* Calls `main`
* Infinite loop after return
* Replaces OS-level startup

---

## 6. link.ld (Memory Layout)

```ld
ENTRY(_start)

SECTIONS
{
  . = 0x00000000;

  .text : {
    *(.text*)
  }

  .data : {
    *(.data*)
  }

  .bss : {
    *(.bss*)
  }
}
```

### Explanation:
* Code starts at address `0x0`
* `.text` → instructions
* `.data` → initialized variables
* `.bss` → uninitialized variables

---

## 7. Example C Program

```c
int max(int a, int b) {
    return (a > b) ? a : b;
}

int main() {
    int m;
    int a = 1;
    int b = 49;
    int c = 4;
    int d = 3;
    int e = 67;

    m = max(a,b);
    m = max(m,c);
    m = max(m,d);
    m = max(m,e);

    return m;
}
```

---

## 8. Generated Assembly (Key Sections)

### Entry Point
```assembly
00000000 <_start>:
   0:   jal     3c <main>
   4:   j       4 <_start+0x4>
```
* Calls `main`
* Infinite loop

### max Function
```assembly
00000008 <max>:
   addi sp,sp,-32
   sw   s0,28(sp)
   addi s0,sp,32
```
* Stack frame created
* Arguments stored
* Comparison: `bge a5,a4,2c`
* Returns result in `a0`

### main Function
```assembly
0000003c <main>:
   addi sp,sp,-48
   sw   ra,44(sp)
   sw   s0,40(sp)
```

**Key operations:**
* Load constants:
  ```assembly
  li a5,1
  li a5,49
  li a5,4
  li a5,3
  li a5,67
  ```
* Function calls: `jal 8 <max>`
* Store intermediate result: `sw a0,-40(s0)`
* Return: 
  ```assembly
  mv a0,a5
  ret
  ```

---

## 9. Key Observations

* Function calls use `jal`
* Return values stored in `a0`
* Stack is used for local variables
* Each `max()` call:
  * creates stack frame
  * compares values
  * returns result

---



---

## 11. Summary

**Flow:**
`C code` → `GCC` → `Object files` → `Linker` → `ELF` → `Binary` → `Hex` → `Verilog`

**Components:**
* `start.S` → entry point
* `main.c` → program logic
* `link.ld` → memory layout
* `build.sh` → full build pipeline
* `hex_to_verilog.py` → For verilog core

