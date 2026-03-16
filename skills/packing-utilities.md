# Pwntools Packing: Byte Manipulation Utilities

## Overview

The `packing` module provides utilities for converting between integers and bytes, essential for exploit development.

## Basic Packing

```python
from pwn import *

# Pack integer to bytes (little-endian by default)
p64(0x41414141)           # 8 bytes
p32(0x41414141)           # 4 bytes
p16(0x4141)               # 2 bytes
p8(0x41)                  # 1 byte

# Pack with big-endian
p64(0x41414141, endian='big')
```

## Unpacking

```python
# Unpack bytes to integer
u64(b'\x41\x41\x41\x41\x41\x41\x41\x41')
u32(b'\x41\x41\x41\x41')
u16(b'\x41\x41')
u8(b'\x41')

# Unpack with big-endian
u64(data, endian='big')
```

## Context-Aware Packing

```python
context(arch='amd64')
p64(0x41414141)  # Uses 64-bit

context(arch='i386')
p32(0x41414141)  # Uses 32-bit
```

## Common Patterns

### Build ROP Payload

```python
# Buffer + canary + saved rbp + return address
payload = b'A' * 100
payload += p64(canary)
payload += p64(0x0)  # saved rbp
payload += p64(rop_gadget)
```

### Leak Parsing

```python
# Receive 8 bytes and convert to address
data = p.recv(8)
addr = u64(data)
print(hex(addr))
```

### Multi-Value Payload

```python
payload = b''
payload += p64(0x41414141)
payload += p64(0x42424242)
payload += p64(0x43434343)
```

## Signed vs Unsigned

```python
# Unsigned (default)
p64(0xffffffffffffffff)

# Signed (for negative numbers)
p64(-1)  # Same as above
```

## Endianness

```python
# Little-endian (default on x86/x64)
p64(0x0102030405060708)  # b'\x08\x07\x06\x05\x04\x03\x02\x01'

# Big-endian
p64(0x0102030405060708, endian='big')  # b'\x01\x02\x03\x04\x05\x06\x07\x08'
```

## Debugging

```python
# Verify packing
addr = 0x41414141
packed = p64(addr)
unpacked = u64(packed)
assert unpacked == addr

# Print hex
print(packed.hex())
```
