# RV32I46F5SP Demo (Vivado)

RTL sources, testbench, and toolchain flow for an RV32I 5-stage pipelined core with debug and FPGA bring-up on Nexys Video.

## Highlights

- RV32I 5-stage pipeline with hazard detection and forwarding
- Branch logic with predictor module
- CSR, exception, and trap control blocks
- Debug wrapper with PC, instruction, register, and ALU visibility
- FPGA top with buttons, LEDs, and UART debug streaming

## Directory layout

```
.
├─ source modules/        RTL sources and include headers (.v/.vh), constraints (.xdc)
├─ testbench/             SystemVerilog testbench
├─ toolchain/             Bare-metal build flow for Instruction_Memory initialization
├─ Vivado_Netlist/        Vivado-generated netlist output
├─ Phase 1 Submission Reports/
├─ Phase 2 Submission Reports/
├─ Synthesis_Results.pdf
├─ Group3_Genus_Netlist.zip
└─ README.md
```

## Key files

- source modules/46F5SP_SoC_TOP.v
  - FPGA top module: `RV32I46F5SPSoCTOP`
- source modules/RV32I46F_5SP_Debug.v
  - Core + debug wrapper: `RV32I46F5SPDebug`
- source modules/Instruction_Memory.v
  - Instruction memory array with in-file program initialization
- testbench/tb_rv32i46f5spdebug.sv
  - Behavioral testbench with debug trace prints
- source modules/RV32I46F_5SP_Debug_XDC.xdc
  - Nexys Video constraints

## Build (Vivado GUI)

1. Create a new RTL project in Vivado.
2. Add all files from `source modules/` as design sources.
3. Add `source modules/RV32I46F_5SP_Debug_XDC.xdc` as constraints.
4. Set the top module to `RV32I46F5SPSoCTOP`.
5. Run synthesis, implementation, and generate a bitstream.

## Simulation

### Vivado xsim

1. Add `testbench/tb_rv32i46f5spdebug.sv` as a simulation source.
2. Set the simulation top to `tb_rv32i46f5spdebug`.
3. Run behavioral simulation.

### Notes

- The RTL uses `include` with relative paths, so keep all `.v`/`.vh` files together in `source modules/`.
- The testbench prints PC/ALU traces and stops after it sees NOPs past the last programmed PC.

## Programming Instruction Memory

The core currently boots from the `data[]` array inside `source modules/Instruction_Memory.v`.

Use the bare-metal toolchain flow in `toolchain/` to generate Verilog-formatted words:

```bash
cd toolchain
chmod +x build.sh
./build.sh
```

The script emits Verilog-style `data[index] = 32'hXXXXXXXX;` lines. Paste them into `Instruction_Memory.v` (replacing the existing program image).

## Toolchain Requirements

- RISC-V GNU toolchain: `gcc-riscv64-unknown-elf`
- Python 3 (for `hex_to_verilog.py`)

See `toolchain/README.md` for the full bare-metal flow and details on `build.sh`, `start.S`, and `link.ld`.

## FPGA I/O (Nexys Video)

The FPGA top exposes:

- Buttons for single-step, continuous run, and debug UART triggers
- LEDs for instruction bit visibility
- UART TX for debug streaming (PC, instruction, register writes, ALU result)

## Artifacts

- Synthesis results in `Synthesis_Results.pdf`
- Gate-level netlists in `Vivado_Netlist/` and `Group3_Genus_Netlist.zip`
