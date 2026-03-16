# Troubleshooting: Common Pwntools Issues

This document covers common problems and solutions when using pwntools.

## Communication Issues

### Process Exits Immediately

**Problem**: Process exits before you can send data

**Solutions**:
```python
# Check if binary exists and is executable
import os
if not os.path.exists('./binary'):
    print("Binary not found")

# Check binary permissions
os.chmod('./binary', 0o755)

# Use timeout to catch early exit
p = process('./binary', timeout=5)
try:
    p.sendline(b'input')
except EOFError:
    print("Process exited")
    print(p.recvall())
```

### Timeout Waiting for Response

**Problem**: `recv()` hangs or times out

**Solutions**:
```python
# Increase timeout
p = process('./binary', timeout=10)

# Use recvline with timeout
try:
    line = p.recvline(timeout=5)
except Timeout:
    print("Timeout waiting for response")

# Check if process is still running
if p.poll() is not None:
    print(f"Process exited with code {p.poll()}")
    print(p.recvall())
```

### Connection Refused (Remote)

**Problem**: Cannot connect to remote service

**Solutions**:
```python
# Verify host and port
HOST = 'example.com'
PORT = 1337

# Test connectivity
import socket
try:
    socket.create_connection((HOST, PORT), timeout=5)
    print("Connection successful")
except socket.error as e:
    print(f"Connection failed: {e}")

# Use remote with timeout
r = remote(HOST, PORT, timeout=10)
```

## Binary Analysis Issues

### Symbol Not Found

**Problem**: `elf.symbols['function']` raises KeyError

**Solutions**:
```python
# Check if symbol exists
elf = ELF('./binary')
if 'system' in elf.symbols:
    system_addr = elf.symbols['system']
else:
    print("Symbol not found")
    print("Available symbols:", list(elf.symbols.keys())[:10])

# Binary may be stripped
print(elf.checksec())

# Use DynELF for runtime resolution
def leak(addr):
    # Implement leak function
    pass

d = DynELF(leak, elf=elf)
system_addr = d.lookup('system', 'libc')
```

### PLT/GOT Not Available

**Problem**: `elf.plt['puts']` or `elf.got['puts']` fails

**Solutions**:
```python
# Check if binary is dynamically linked
elf = ELF('./binary')
print(elf.checksec())

# List available PLT entries
print("PLT entries:", list(elf.plt.keys()))

# List available GOT entries
print("GOT entries:", list(elf.got.keys()))

# Binary may be statically linked
if not elf.plt:
    print("Binary is statically linked")
```

### Checksec Shows Unexpected Protections

**Problem**: Protections don't match expectations

**Solutions**:
```python
# Print full checksec output
elf = ELF('./binary')
print(elf.checksec())

# Check individual protections
print(f"NX: {elf.nx}")
print(f"PIE: {elf.pie}")
print(f"Canary: {elf.canary}")
print(f"RELRO: {elf.relro}")

# Protections may be applied at runtime
# Check with `checksec` command
import subprocess
result = subprocess.run(['checksec', '--file=./binary'], capture_output=True)
print(result.stdout.decode())
```

## Exploitation Issues

### Offset Finding Fails

**Problem**: `cyclic_find()` returns wrong offset

**Solutions**:
```python
# Verify crash address
# Use GDB to get exact crash address
# gdb ./binary
# run
# (binary crashes)
# info registers
# Look for rip/eip value

# Verify pattern size is large enough
pattern = cyclic(500)  # Increase size

# Check for alignment issues
# Some binaries require aligned addresses
offset = cyclic_find(crash_addr)
if offset % 8 != 0:
    print(f"Offset {offset} is not 8-byte aligned")

# Verify crash address is from pattern
if crash_addr not in [u32(cyclic(i)[i:i+4]) for i in range(0, 200, 4)]:
    print("Crash address not from pattern")
```

### ROP Chain Not Working

**Problem**: ROP chain doesn't execute correctly

**Solutions**:
```python
# Print ROP chain to verify
rop = ROP(elf)
rop.call('system', [arg])
print(rop.dump())

# Verify gadgets exist
print(f"pop rdi gadget: {rop.rdi}")

# Check for null bytes in chain
chain = rop.chain()
if b'\x00' in chain:
    print("Warning: Null bytes in ROP chain")

# Verify argument addresses
bin_sh = next(elf.search(b'/bin/sh'))
print(f"/bin/sh at: {hex(bin_sh)}")

# Use GDB to debug ROP execution
p = process('./binary')
gdb.attach(p, '''
    break *0x400000
    continue
    stepi
''')
```

### Shellcode Not Executing

**Problem**: Shellcode doesn't execute or crashes

**Solutions**:
```python
# Verify shellcode generation
context(arch='amd64', os='linux')
shellcode = asm(shellcraft.sh())
print(f"Shellcode size: {len(shellcode)}")
print(f"Shellcode hex: {shellcode.hex()}")

# Check for null bytes
if b'\x00' in shellcode:
    print("Warning: Null bytes in shellcode")

# Verify shellcode is executable
# Use mprotect if needed
rop = ROP(elf)
rop.call('mprotect', [shellcode_addr & ~0xfff, 0x1000, 7])
rop.call('jmp', [shellcode_addr])

# Test shellcode locally
# Write to file and execute
with open('/tmp/test.bin', 'wb') as f:
    f.write(shellcode)
# Execute and verify
```

## Format String Issues

### Offset Finding Fails

**Problem**: `FmtStr` can't find offset

**Solutions**:
```python
# Verify leak function works
def exec_fmt(payload):
    p = process('./binary')
    p.sendline(payload)
    return p.recvall()

# Test manually
result = exec_fmt(b'%x.%x.%x.%x')
print(result)

# If no output, binary may not be vulnerable
# Try different format strings
for i in range(20):
    result = exec_fmt(b'%' + str(i).encode() + b'$x')
    print(f"Offset {i}: {result}")

# Use FmtStr with timeout
autofmt = FmtStr(exec_fmt, timeout=5)
```

### Memory Write Fails

**Problem**: `fmtstr_payload()` doesn't write correctly

**Solutions**:
```python
# Verify offset is correct
offset = 6  # Adjust based on binary

# Test with simple write
payload = fmtstr_payload(offset, {0x601234: 0x41414141})
print(f"Payload size: {len(payload)}")

# Verify target address is writable
# Use GDB to check memory permissions
# gdb ./binary
# vmmap
# Look for writable sections

# Try writing to different address
payload = fmtstr_payload(offset, {elf.got['puts']: 0xdeadbeef})

# Check for null bytes in address
if b'\x00' in p64(target_addr):
    print("Target address contains null bytes")
    # Use alternative address or technique
```

## ASLR/PIE Issues

### Exploit Works Locally But Not Remotely

**Problem**: Hardcoded addresses don't work on remote

**Solutions**:
```python
# Check if ASLR is enabled
# Local: cat /proc/sys/kernel/randomize_va_space
# Remote: assume it's enabled

# Leak addresses instead of hardcoding
def leak_libc():
    p = process('./binary')
    # Use format string or other leak
    p.sendline(b'%6$p')  # Leak stack value
    leaked = int(p.recvline().strip(), 16)
    return leaked

# Use DynELF for automatic resolution
def leak(addr):
    p = process('./binary')
    # Implement leak
    return leaked_bytes

d = DynELF(leak, elf=ELF('./binary'))
system_addr = d.lookup('system', 'libc')
```

### PIE Makes Addresses Unpredictable

**Problem**: Binary addresses change on each run

**Solutions**:
```python
# Check if PIE is enabled
elf = ELF('./binary')
print(f"PIE: {elf.pie}")

# If PIE is enabled, leak binary base
# Use information disclosure to leak code address
# Calculate offset from leaked address

# Example: leak main() address
leaked_main = leak_address()
elf_base = leaked_main - elf.symbols['main']

# Recalculate all addresses
win_addr = elf_base + elf.symbols['win']
```

## Packing Issues

### Null Bytes in Payload

**Problem**: Payload contains null bytes that truncate input

**Solutions**:
```python
# Check for null bytes
payload = p64(0x41414141)
if b'\x00' in payload:
    print("Payload contains null bytes")

# Use alternative addresses
# Avoid addresses with null bytes
for addr in range(0x400000, 0x401000):
    if b'\x00' not in p64(addr):
        print(f"Valid address: {hex(addr)}")

# Use short writes for format strings
# Instead of %n (4 bytes), use %hn (2 bytes)
payload = fmtstr_payload(offset, {addr: value}, write_size='short')
```

### Endianness Issues

**Problem**: Packed values are in wrong byte order

**Solutions**:
```python
# Verify endianness
print(f"Endianness: {context.endian}")

# Check binary endianness
elf = ELF('./binary')
print(f"Binary endianness: {elf.endian}")

# Set context to match binary
context(arch='amd64', endian='little')

# Verify packing
addr = 0x41414141
packed = p64(addr)
unpacked = u64(packed)
assert unpacked == addr
```

## Debugging Techniques

### Enable Verbose Logging

```python
# Maximum verbosity
context.log_level = 'debug'

# Log specific operations
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Use GDB for Complex Issues

```python
# Attach GDB with custom script
gdb_script = '''
break main
continue
x/20x $rsp
info registers
backtrace
'''

p = process('./binary')
gdb.attach(p, gdb_script)
p.interactive()
```

### Print Intermediate Values

```python
# Debug payload construction
offset = 100
target = 0x601234
value = 0x41414141

payload = b'A' * offset + p64(target) + p64(value)
print(f"Payload length: {len(payload)}")
print(f"Payload hex: {payload.hex()}")

# Verify structure
print(f"Offset section: {payload[:offset].hex()}")
print(f"Target address: {payload[offset:offset+8].hex()}")
print(f"Value: {payload[offset+8:offset+16].hex()}")
```

## Performance Issues

### Slow Gadget Finding

**Problem**: ROP gadget search takes too long

**Solutions**:
```python
# Cache ROP object
rop = ROP(elf)
# Gadget finding happens on first access
pop_rdi = rop.rdi  # Slow first time
pop_rdi = rop.rdi  # Fast second time (cached)

# Use smaller binary if possible
# Strip unnecessary sections
# Use pre-computed gadgets

# Limit gadget search
rop = ROP(elf, base=0x400000, max_gadgets=1000)
```

### Slow DynELF Resolution

**Problem**: DynELF takes too long to resolve symbols

**Solutions**:
```python
# Cache results
d = DynELF(leak, elf=ELF('./binary'))
system_addr = d.lookup('system', 'libc')
# Results are cached automatically

# Resolve only needed symbols
system_addr = d.lookup('system', 'libc')
# Don't resolve all symbols

# Use precomputed libc base if available
libc_base = 0x7ffff7a00000
system_addr = libc_base + 0x50d60  # Offset from known libc version
```

## Getting Help

If you encounter issues not covered here:

1. **Check official documentation**: https://docs.pwntools.com/
2. **Search GitHub issues**: https://github.com/Gallopsled/pwntools/issues
3. **Ask on Discord**: https://discord.gg/96VA2zvjCB
4. **Review write-ups**: https://github.com/Gallopsled/pwntools-write-ups
