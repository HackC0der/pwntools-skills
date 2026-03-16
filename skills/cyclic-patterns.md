# Pwntools Cyclic: Pattern Generation & Offset Finding

## Overview

The `cyclic` module generates unique patterns to find buffer overflow offsets and crash addresses.

## Generate Patterns

```python
from pwn import *

# Generate cyclic pattern
pattern = cyclic(100)  # 100 bytes of unique pattern

# Pattern looks like: aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawaaaxaaayaaazaabbaabcaabdaabea...
```

## Find Offset

### From Crash Address

```python
# Send pattern to binary
p = process('./binary')
p.sendline(cyclic(100))
p.wait()

# Get crash address (from gdb or core dump)
crash_addr = 0x61616161

# Find offset
offset = cyclic_find(crash_addr)
print(f"Offset: {offset}")  # Output: Offset: 12
```

### From Received Data

```python
# Binary echoes back part of input
p = process('./binary')
p.sendline(cyclic(100))
echoed = p.recvline()

# Find offset of echoed data
offset = cyclic_find(echoed[:4])
print(f"Offset: {offset}")
```

## Common Patterns

### Buffer Overflow Exploitation

```python
# 1. Find offset
pattern = cyclic(200)
p = process('./binary')
p.sendline(pattern)
# Crash and get address

# 2. Calculate payload
offset = cyclic_find(crash_addr)
payload = b'A' * offset + p64(rop_gadget)
p = process('./binary')
p.sendline(payload)
p.interactive()
```

### Stack Canary Bypass

```python
# 1. Find canary offset
pattern = cyclic(200)
p = process('./binary')
p.sendline(pattern)
canary_bytes = p.recv(8)

# 2. Find offset
canary_offset = cyclic_find(canary_bytes)
print(f"Canary at offset: {canary_offset}")
```

### Format String Offset

```python
# 1. Generate pattern
pattern = cyclic(100)

# 2. Send as format string
p = process('./binary')
p.sendline(b'%x.' * 20 + pattern)
output = p.recvline()

# 3. Find offset from output
offset = cyclic_find(output)
```

## Debugging

```python
# Verify pattern
pattern = cyclic(100)
offset = 12

# Extract 4 bytes at offset
chunk = pattern[offset:offset+4]
found_offset = cyclic_find(chunk)
assert found_offset == offset
```

## Tips

- Use larger patterns (200-500 bytes) for complex binaries
- Combine with gdb for precise offset finding
- Use `cyclic_find()` with exact crash bytes for accuracy
- Pattern is deterministic - same input always produces same pattern
