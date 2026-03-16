# Pwntools Context: Global Configuration

## Overview

The `context` object manages global settings for architecture, OS, logging, and other pwntools behavior.

## Architecture & OS Configuration

```python
from pwn import *

# Set architecture and OS
context(arch='amd64', os='linux')
context(arch='i386', os='linux')
context(arch='arm', os='linux')
context(arch='mips', os='linux')

# Supported architectures
# amd64, i386, arm, thumb, mips, mips64, ppc, ppc64, sparc, sparc64, aarch64, riscv64

# Supported OS
# linux, freebsd, windows
```

## Logging Configuration

```python
# Set log level
context.log_level = 'debug'    # Verbose output
context.log_level = 'info'     # Normal output
context.log_level = 'warning'  # Warnings only
context.log_level = 'error'    # Errors only

# Quiet mode (suppress output)
context.log_level = 'critical'

# Or use decorator
@context.quiet
def exploit():
    p = process('./binary')
    p.sendline(b'input')
```

## Binary Configuration

```python
# Set binary for context
context.binary = ELF('./binary')

# Access binary from context
elf = context.binary
print(elf.symbols['main'])
```

## Bytes & Endianness

```python
# Set byte size (automatically set by arch)
context.bytes = 8  # 64-bit
context.bytes = 4  # 32-bit

# Endianness (automatically set by arch)
context.endian = 'little'
context.endian = 'big'

# Packing functions use context
p64(0x41414141)  # Uses context.bytes and context.endian
```

## Newline Configuration

```python
# Set newline character
context.newline = b'\n'      # Default
context.newline = b'\r\n'    # Windows style
context.newline = b'\x00'    # Null byte
```

## Terminal Configuration

```python
# Terminal type
context.terminal = ['tmux', 'new-window', '-n', 'gdb', '-c', '{cwd}']
context.terminal = ['xterm', '-e']
context.terminal = ['gnome-terminal', '--']

# Used by gdb.attach() and gdb.debug()
```

## Timeout Configuration

```python
# Set default timeout
context.timeout = 5  # 5 seconds
context.timeout = None  # No timeout
```

## Common Patterns

### Multi-Architecture Exploit

```python
def exploit(arch):
    context(arch=arch, os='linux')

    # Code works for all architectures
    shellcode = asm(shellcraft.sh())
    print(f"{arch}: {len(shellcode)} bytes")

for arch in ['amd64', 'i386', 'arm', 'mips']:
    exploit(arch)
```

### Temporary Context Change

```python
# Save current context
old_arch = context.arch

# Change temporarily
context(arch='i386')
shellcode = asm(shellcraft.sh())

# Restore
context(arch=old_arch)
```

### Clear Context

```python
# Reset to defaults
context.clear()

# Or set specific values
context.clear(arch='amd64', os='linux')
```

## Debugging

```python
# Print current context
print(context)

# Check specific settings
print(context.arch)
print(context.bits)
print(context.bytes)
print(context.endian)
```

## Advanced: Custom Context

```python
# Create custom context for specific binary
context(arch='amd64', os='linux', log_level='debug')
context.binary = ELF('./binary')

# All subsequent operations use this context
elf = context.binary
shellcode = asm(shellcraft.sh())
```
