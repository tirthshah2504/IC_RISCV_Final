# RV32I46F5SP Demo (Vivado)

This repo contains the RTL sources, constraints, and testbench for the RV32I46F5SP demo.

## Directory layout

```
repo/
  source modules/    RTL sources, include headers (.v, .vh), and constraints (.xdc)
  testbench/         Testbenches (.sv)
  README.md
```

## Key files

- source modules/46F5SP_SoC_TOP.v
  - FPGA top module: RV32I46F5SPSoCTOP
- source modules/RV32I46F_5SP_Debug.v
  - Core + debug wrapper module: RV32I46F5SPDebug
- testbench/tb_rv32i46f5spdebug.sv
  - Behavioral testbench for RV32I46F5SPDebug
- source modules/RV32I46F_5SP_Debug_XDC.xdc
  - Nexys Video constraints

## Build (Vivado GUI)

1. Open Vivado and create a new RTL project.
2. Add all files in source modules/ as design sources.
3. Add source modules/RV32I46F_5SP_Debug_XDC.xdc as constraints.
4. Set the top module to RV32I46F5SPSoCTOP.
5. Run synthesis, implementation, and generate the bitstream.

## Simulation (Vivado xsim)

1. Add testbench/tb_rv32i46f5spdebug.sv as a simulation source.
2. Set the simulation top module to tb_rv32i46f5spdebug.
3. Run behavioral simulation.

Notes:
- The RTL uses `include` with relative paths, so keep all .v/.vh files together in source modules/.
- The testbench prints PC/ALU traces and stops after it sees NOPs past the last programmed PC.
