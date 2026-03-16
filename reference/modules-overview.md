# Reference: Pwntools Modules Overview

This document provides a comprehensive overview of pwntools modules and their relationships.

## Module Hierarchy

```
pwnlib/
├── tubes/              # Communication
│   ├── tube.py        # Base class
│   ├── process.py     # Local processes
│   ├── remote.py      # Remote sockets
│   ├── ssh.py         # SSH connections
│   └── listen.py      # Server sockets
├── elf/               # Binary analysis
│   ├── elf.py         # ELF parsing
│   └── corefile.py    # Core dump analysis
├── rop/               # ROP gadgets
│   ├── rop.py         # ROP chain building
│   ├── gadgets.py     # Gadget finding
│   └── ret2dlresolve.py # ret2dlresolve
├── shellcraft/        # Shellcode generation
│   ├── amd64.py       # x86-64 shellcode
│   ├── i386.py        # x86 shellcode
│   ├── arm.py         # ARM shellcode
│   └── ...            # Other architectures
├── util/              # Utilities
│   ├── packing.py     # p64, u64, etc.
│   ├── cyclic.py      # Cyclic patterns
│   ├── fiddling.py    # Bit manipulation
│   └── ...
├── fmtstr.py          # Format string exploitation
├── asm.py             # Assembly/disassembly
├── gdb.py             # GDB integration
├── dynelf.py          # Dynamic ELF resolution
└── context.py         # Global configuration
```

## Core Modules

### Communication (tubes)

**Purpose**: Unified interface for process/socket/SSH communication

**Key Classes**:
- `tube` - Base class with common methods
- `process` - Local process interaction
- `remote` - TCP socket communication
- `ssh` - SSH connections
- `listen` - Server socket

**Common Methods**:
- `send()`, `sendline()`, `sendafter()`
- `recv()`, `recvline()`, `recvuntil()`, `recvexactly()`
- `interactive()` - Full control to user
- `close()`, `kill()` - Process control

### Binary Analysis (elf)

**Purpose**: Parse and analyze ELF binaries

**Key Classes**:
- `ELF` - Main class for binary analysis
- `Function` - Function information
- `Section` - Section information

**Key Properties**:
- `symbols` - Symbol table
- `plt` - PLT entries
- `got` - GOT entries
- `sections` - Binary sections
- `segments` - Program segments

**Key Methods**:
- `checksec()` - Check protections
- `search()` - Find bytes in binary
- `get_section_by_name()` - Get section

### ROP (rop)

**Purpose**: Build ROP chains automatically

**Key Classes**:
- `ROP` - ROP chain builder
- `Gadget` - Individual gadget

**Key Methods**:
- `call()` - Call function with arguments
- `raw()` - Add raw value
- `chain()` - Get final payload
- `dump()` - Print chain

**Magic Properties**:
- `rop.rdi`, `rop.rsi`, etc. - Register gadgets
- `rop.read`, `rop.write`, etc. - Function calls

### Shellcode (shellcraft)

**Purpose**: Generate platform-specific shellcode

**Key Functions**:
- `shellcraft.sh()` - /bin/sh shell
- `shellcraft.exit(code)` - Exit syscall
- `shellcraft.read()`, `shellcraft.write()` - I/O
- `shellcraft.execve()` - Execute command
- `shellcraft.mprotect()` - Change memory protection

**Usage**:
```python
context(arch='amd64', os='linux')
shellcode = shellcraft.sh()
code = asm(shellcode)
```

### Utilities (util)

**Packing** (`packing.py`):
- `p64()`, `p32()`, `p16()`, `p8()` - Pack to bytes
- `u64()`, `u32()`, `u16()`, `u8()` - Unpack from bytes

**Cyclic** (`cyclic.py`):
- `cyclic(length)` - Generate pattern
- `cyclic_find(data)` - Find offset

**Fiddling** (`fiddling.py`):
- Bit manipulation utilities
- XOR, rotate, etc.

### Format Strings (fmtstr.py)

**Purpose**: Automate format string exploitation

**Key Classes**:
- `FmtStr` - Automated format string exploitation

**Key Functions**:
- `fmtstr_payload()` - Generate payload
- `fmtstr_read()` - Read memory

**Usage**:
```python
def exec_fmt(payload):
    p = process('./binary')
    p.sendline(payload)
    return p.recvall()

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset
```

### Assembly (asm.py)

**Purpose**: Assemble and disassemble code

**Key Functions**:
- `asm()` - Assemble to bytes
- `disasm()` - Disassemble to assembly

**Usage**:
```python
context(arch='amd64')
code = asm('mov rax, 0x41414141')
print(disasm(code))
```

### GDB Integration (gdb.py)

**Purpose**: Debug binaries with GDB

**Key Functions**:
- `gdb.attach()` - Attach to running process
- `gdb.debug()` - Start with GDB

**Usage**:
```python
p = process('./binary')
gdb.attach(p, 'break main')
```

### Dynamic ELF (dynelf.py)

**Purpose**: Resolve libc symbols at runtime

**Key Classes**:
- `DynELF` - Runtime symbol resolution

**Usage**:
```python
def leak(addr):
    # Leak bytes at address
    return leaked_bytes

d = DynELF(leak, elf=ELF('./binary'))
system_addr = d.lookup('system', 'libc')
```

### Context (context.py)

**Purpose**: Global configuration

**Key Settings**:
- `arch` - Architecture (amd64, i386, arm, etc.)
- `os` - Operating system (linux, freebsd, windows)
- `bits` - Bit width (32, 64)
- `bytes` - Byte size (4, 8)
- `endian` - Endianness (little, big)
- `log_level` - Logging level
- `timeout` - Default timeout
- `binary` - Current binary

**Usage**:
```python
context(arch='amd64', os='linux', log_level='debug')
```

## Workflow Integration

### Typical Exploitation Workflow

1. **Analyze Binary**
   ```python
   elf = ELF('./binary')
   elf.checksec()
   ```

2. **Find Offset**
   ```python
   pattern = cyclic(200)
   offset = cyclic_find(crash_addr)
   ```

3. **Build Exploit**
   ```python
   rop = ROP(elf)
   rop.call('system', [arg])
   payload = b'A' * offset + rop.chain()
   ```

4. **Send Payload**
   ```python
   p = process('./binary')
   p.sendline(payload)
   p.interactive()
   ```

5. **Debug if Needed**
   ```python
   gdb.attach(p, 'break main')
   ```

## Architecture Support

Each module supports multiple architectures:

- **x86**: amd64, i386
- **ARM**: arm, thumb, aarch64
- **MIPS**: mips, mips64
- **PowerPC**: ppc, ppc64
- **SPARC**: sparc, sparc64
- **RISC-V**: riscv64

Set architecture with:
```python
context(arch='amd64')
```

## Common Patterns

### Information Leak
```python
# Format string leak
payload = b'%' + str(offset).encode() + b'$p'
p.sendline(payload)
leaked = int(p.recvline().strip(), 16)
```

### Memory Write
```python
# Format string write
payload = fmtstr_payload(offset, {addr: value})
p.sendline(payload)
```

### Shellcode Injection
```python
shellcode = asm(shellcraft.sh())
payload = b'A' * offset + shellcode
p.sendline(payload)
```

### ROP Chain
```python
rop = ROP(elf)
rop.call('system', [bin_sh_addr])
payload = b'A' * offset + rop.chain()
p.sendline(payload)
```

## Performance Considerations

- **DynELF**: Multiple leaks required, cache results
- **ROP**: Gadget finding can be slow on large binaries
- **Shellcraft**: Code generation is fast
- **Packing**: Minimal overhead

## Error Handling

Common exceptions:
- `EOFError` - Process exited
- `PwnlibException` - Pwntools error
- `Timeout` - Operation timed out

Handle gracefully:
```python
try:
    p.sendline(payload)
    response = p.recvline()
except EOFError:
    print("Process exited")
except Timeout:
    print("Timeout")
```
