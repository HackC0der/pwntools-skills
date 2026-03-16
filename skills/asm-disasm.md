# Pwntools Assembly & Disassembly

## Overview

The `asm()` and `disasm()` functions convert between assembly code and machine code, supporting multiple architectures.

## Assembly

### Basic Assembly

```python
from pwn import *

context(arch='amd64', os='linux')

# Assemble single instruction
code = asm('mov rax, 0x41414141')
print(code.hex())

# Assemble multiple instructions
code = asm('''
    mov rax, 0x41414141
    mov rbx, 0x42424242
    ret
''')
```

### Architecture-Specific Assembly

```python
# 64-bit x86
context(arch='amd64')
code = asm('pop rdi; ret')

# 32-bit x86
context(arch='i386')
code = asm('pop eax; ret')

# ARM
context(arch='arm')
code = asm('mov r0, #0x41')

# MIPS
context(arch='mips')
code = asm('li $a0, 0x41')
```

## Disassembly

### Basic Disassembly

```python
context(arch='amd64', os='linux')

# Disassemble bytes
code = b'\x48\xc7\xc0\x41\x41\x41\x41'
asm_code = disasm(code)
print(asm_code)
# Output:
#    0:	48 c7 c0 41 41 41 41 	mov    rax,0x41414141
```

### Disassemble with Address

```python
code = b'\x48\xc7\xc0\x41\x41\x41\x41'
asm_code = disasm(code, vma=0x400000)
print(asm_code)
# Output:
#    0x400000:	48 c7 c0 41 41 41 41 	mov    rax,0x41414141
```

## Shellcraft Integration

### Generate Shellcode

```python
context(arch='amd64', os='linux')

# Generate /bin/sh shell
shellcode = shellcraft.sh()
code = asm(shellcode)

# Generate exit
shellcode = shellcraft.exit(0)
code = asm(shellcode)

# Generate syscall
shellcode = shellcraft.syscall('SYS_write', 1, 'rsp', 100)
code = asm(shellcode)
```

### View Generated Shellcode

```python
context(arch='amd64', os='linux')

# Generate and view
shellcode = shellcraft.sh()
print(shellcode)  # Print assembly

code = asm(shellcode)
print(disasm(code))  # Print disassembly
```

## Common Patterns

### Build ROP Gadget

```python
context(arch='amd64')

# Assemble gadget
gadget = asm('pop rdi; ret')
print(gadget.hex())

# Use in exploit
payload = b'A' * 100 + gadget
```

### Inline Assembly in Exploit

```python
context(arch='amd64', os='linux')

# Assemble inline
payload = b'A' * 100
payload += asm('pop rdi; ret')
payload += p64(0xdeadbeef)
payload += asm('jmp rax')
```

### Multi-Architecture Shellcode

```python
def get_shellcode(arch):
    context(arch=arch, os='linux')
    return asm(shellcraft.sh())

for arch in ['amd64', 'i386', 'arm']:
    code = get_shellcode(arch)
    print(f"{arch}: {len(code)} bytes")
```

## Debugging

```python
# Print assembly
context(arch='amd64')
code = asm('mov rax, 0x41414141')
print(code.hex())

# Print disassembly
print(disasm(code))

# Verify round-trip
original = 'mov rax, 0x41414141'
code = asm(original)
disassembled = disasm(code)
print(disassembled)
```

## Common Issues

### Architecture Mismatch
- Set `context(arch='...')` before assembling
- Verify target binary architecture
- Use correct register names for architecture

### Null Bytes in Shellcode
- Use `asm()` with `avoid` parameter (if supported)
- Use alternative instructions
- Encode shellcode after assembly

### Unsupported Instructions
- Check architecture support
- Use alternative instructions
- Verify syntax
