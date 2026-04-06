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