# Pwntools Tubes: Process & Network Communication

## Overview

The `tubes` module provides unified interfaces for communicating with:
- Local processes (`process`)
- Remote services (`remote`)
- SSH connections (`ssh`)

All tube types inherit from `pwnlib.tubes.tube.tube` and share a common API.

## Process Communication

### Basic Usage

```python
from pwn import *

# Start local process
p = process('./binary')

# Send data
p.send(b'data')              # No newline
p.sendline(b'data')          # With newline
p.sendafter(b'prompt>', b'input')  # Send after pattern
p.sendlineafter(b'>', b'input')    # Sendline after pattern

# Receive data
data = p.recv(1024)          # Read up to 1024 bytes
line = p.recvline()          # Read until newline
data = p.recvuntil(b'$')     # Read until pattern
data = p.recvexactly(100)    # Read exactly 100 bytes
all_data = p.recvall()       # Read until EOF

# Interactive mode
p.interactive()              # Full control to user
```

### Process Control

```python
# Check if running
status = p.poll()            # None if running, exit code if stopped

# Wait for process
exit_code = p.wait()

# Kill process
p.kill()

# Close connection
p.close()

# Context manager (auto-close)
with process('./binary') as p:
    p.sendline(b'input')
    p.recvline()
```

### Timeout & Error Handling

```python
p = process('./binary', timeout=5)

try:
    p.sendline(b'input')
    response = p.recvline()
except EOFError:
    print("Process exited")
except pwnlib.exception.PwnlibException as e:
    print(f"Error: {e}")
```

## Remote Communication

```python
# Connect to remote service
r = remote('example.com', 1337)

# Same interface as process
r.sendline(b'command')
response = r.recvline()

r.close()

# With timeout
r = remote('example.com', 1337, timeout=10)
```

## SSH Connections

```python
s = ssh(host='example.com', user='user', password='pass')

# Execute command
output = s.process('ls -la').recvall()

# Interactive shell
s.interactive()

# File operations
s.put('local.txt', 'remote.txt')
s.get('remote.txt', 'local.txt')

# Run command and get output
output = s.run('cat /etc/passwd').recvall()
```

## Common Patterns

### Leak Information
```python
p = process('./binary')
p.recvuntil(b'Address: ')
leaked_addr = int(p.recvline().strip(), 16)
```

### Send Payload with Timing
```python
payload = b'A' * 100 + p64(0xdeadbeef)
p.sendline(payload)
time.sleep(0.1)
response = p.recvline()
```

### Interact Until Pattern
```python
p.sendline(b'command')
output = p.recvuntil(b'$', timeout=2)
```

### Multiple Interactions
```python
p = process('./binary')
p.recvuntil(b'Name: ')
p.sendline(b'Alice')
p.recvuntil(b'Age: ')
p.sendline(b'25')
result = p.recvall()
```

## Debugging

```python
# Enable verbose output
context.log_level = 'debug'

# Check process status
print(p.poll())  # None if running, exit code if stopped

# Kill process
p.kill()

# Print received data
data = p.recv(100)
print(data)
print(enhex(data))  # Hex representation
```

## Advanced: Newline Handling

```python
# Custom newline character
p = process('./binary')
p.newline = b'\r\n'

# Or set globally
context.newline = b'\r\n'
```
