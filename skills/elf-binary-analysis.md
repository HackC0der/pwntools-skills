# Pwntools ELF: Binary Analysis & Symbol Resolution

## Overview

The `ELF` class provides utilities for parsing and analyzing ELF binaries, finding gadgets, symbols, and memory addresses.

## Basic Usage

```python
from pwn import *

elf = ELF('./binary')

# Get symbol addresses
main_addr = elf.symbols['main']
printf_addr = elf.symbols['printf']

# Get section addresses
text_addr = elf.get_section_by_name('.text').header['sh_addr']

# Get PLT/GOT entries
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
```

## Finding Gadgets & Strings

```python
# Find ROP gadgets
gadgets = elf.search(b'pop rdi; ret')

# Find strings
bin_sh = next(elf.search(b'/bin/sh'))

# Find all occurrences
for addr in elf.search(b'pattern'):
    print(hex(addr))
```

## Binary Properties

```python
# Check protections
print(elf.checksec())
# Output:
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# Get architecture
print(elf.arch)  # 'amd64'

# Check if 32-bit or 64-bit
print(elf.bits)  # 64

# Get base address (for PIE binaries)
print(elf.address)  # 0x0 if not loaded
```

## Sections & Headers

```python
# List all sections
for section in elf.sections:
    print(section.name, hex(section.header['sh_addr']))

# Get specific section
text = elf.get_section_by_name('.text')
print(hex(text.header['sh_addr']), hex(text.header['sh_size']))

# Get segment info
for segment in elf.segments:
    print(segment.header['p_type'], hex(segment.header['p_vaddr']))
```

## Dynamic Linking Info

```python
# Get dynamic symbols
for sym in elf.dynsym:
    print(sym.name, hex(sym['st_value']))

# Get relocation entries
for reloc in elf.relocs:
    print(reloc.name, hex(reloc['r_offset']))
```

## Common Patterns

### Leak GOT Entry
```python
elf = ELF('./binary')
puts_got_addr = elf.got['puts']
# Use format string or other leak to read this address
```

### Find Gadget for ROP
```python
elf = ELF('./binary')
# Find "pop rdi; ret" gadget
pop_rdi = next(elf.search(asm('pop rdi; ret')))
```

### Bypass ASLR with Leak
```python
elf = ELF('./binary')
# Leak libc address from GOT
libc_leak = leak_from_binary()
libc_base = libc_leak - elf.got['puts']
system_addr = libc_base + libc.symbols['system']
```

## Debugging

```python
# Print all symbols
for name, addr in elf.symbols.items():
    print(f"{name}: {hex(addr)}")

# Check if symbol exists
if 'system' in elf.symbols:
    print("system found")
```
