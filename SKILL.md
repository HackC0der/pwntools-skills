# Pwntools Skills Guide

Comprehensive reference for using pwntools in CTF and binary exploitation challenges.

## Core Modules

### 1. Process & Communication
- **pwnlib.tubes.process** - Local process interaction
- **pwnlib.tubes.remote** - Remote socket communication
- **pwnlib.tubes.ssh** - SSH connections

### 2. Binary Analysis
- **pwnlib.elf** - ELF binary parsing and symbol resolution
- **pwnlib.disasm** - Disassembly utilities
- **pwnlib.asm** - Assembly/disassembly
- **pwnlib.dynelf** - Runtime libc symbol resolution

### 3. Exploitation Primitives
- **pwnlib.shellcraft** - Shellcode generation
- **pwnlib.rop** - ROP gadget finding and chaining
- **pwnlib.fmtstr** - Format string exploitation
- **pwnlib.encoders** - Payload encoding

### 4. Utilities
- **pwnlib.util.packing** - Byte packing/unpacking
- **pwnlib.util.cyclic** - Cyclic pattern generation
- **pwnlib.context** - Global configuration
- **pwnlib.gdb** - GDB debugging integration

## Quick Reference

### Basic Setup
```python
from pwn import *
context(arch='amd64', os='linux')
```

### Process Interaction
```python
p = process('./binary')
p.sendline(b'input')
data = p.recv(1024)
p.interactive()
```

### ROP Exploitation
```python
elf = ELF('./binary')
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])
```

### Format String
```python
payload = fmtstr_payload(offset, {address: value})
```

### Shellcode
```python
context(arch='amd64', os='linux')
shellcode = asm(shellcraft.sh())
```

## Skill Files

- **tubes-communication.md** - Process/socket/SSH communication
- **elf-binary-analysis.md** - ELF parsing and symbol resolution
- **packing-utilities.md** - Byte packing/unpacking
- **shellcraft-shellcode.md** - Shellcode generation
- **cyclic-patterns.md** - Pattern generation and offset finding
- **rop-exploitation.md** - ROP chain building
- **format-string-exploitation.md** - Format string bugs
- **context-configuration.md** - Global configuration
- **asm-disasm.md** - Assembly and disassembly
- **gdb-debugging.md** - GDB integration
- **dynelf-libc-resolution.md** - Runtime libc resolution

## Common Exploitation Patterns

### Buffer Overflow with ROP
1. Find offset with cyclic pattern
2. Build ROP chain with ROP class
3. Send payload: buffer + canary + saved_rbp + rop_chain

### Format String Exploitation
1. Find offset with cyclic or FmtStr class
2. Leak information or write memory
3. Use fmtstr_payload() for automated payload generation

### Shellcode Injection
1. Generate shellcode with shellcraft
2. Assemble with asm()
3. Inject into buffer or memory
4. Jump to shellcode

### Bypass ASLR
1. Leak libc address via information disclosure
2. Calculate symbol addresses from leaked base
3. Use DynELF for automatic symbol resolution
4. Build ROP chain with resolved addresses

## Architecture Support

- **amd64** - 64-bit x86
- **i386** - 32-bit x86
- **arm** - ARM 32-bit
- **thumb** - ARM Thumb mode
- **aarch64** - ARM 64-bit
- **mips** - MIPS 32-bit
- **mips64** - MIPS 64-bit
- **ppc** - PowerPC 32-bit
- **ppc64** - PowerPC 64-bit
- **sparc** - SPARC 32-bit
- **sparc64** - SPARC 64-bit
- **riscv64** - RISC-V 64-bit

## Resources

- Official Docs: https://docs.pwntools.com/
- GitHub: https://github.com/Gallopsled/pwntools
- Tutorials: https://github.com/Gallopsled/pwntools-tutorial
- Write-ups: https://github.com/Gallopsled/pwntools-write-ups

