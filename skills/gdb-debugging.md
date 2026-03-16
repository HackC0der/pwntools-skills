# Pwntools GDB: Debugging Integration

## Overview

Pwntools integrates with GDB for debugging binaries during exploitation. Use `gdb.attach()` to attach to running processes or `gdb.debug()` to start with GDB. This is one of the most powerful features for exploit development, allowing you to inspect memory, registers, and execution flow in real-time.

## Why Use gdb.attach()?

**Key Benefits:**
- Debug exploit payloads in real-time
- Inspect memory and registers at any point
- Verify offset calculations
- Trace execution flow
- Catch crashes and analyze root causes
- Validate ROP chains before sending
- Test format string payloads interactively

## Attach to Running Process

### Basic Attach

```python
from pwn import *

p = process('./binary')

# Attach GDB to running process
gdb.attach(p)

# Process pauses, GDB opens in terminal
# Set breakpoints, step through code, etc.
# Type 'continue' in GDB to resume

p.interactive()
```

### Attach with Script (Recommended)

```python
# Run GDB commands automatically
gdb_script = '''
break main
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

p.interactive()
```

**Why use scripts?**
- Automate repetitive debugging steps
- Faster iteration during development
- Reproducible debugging sessions
- Less manual typing in GDB

### Attach with Breakpoint

```python
elf = ELF('./binary')

p = process('./binary')

# Attach and break at main
gdb.attach(p, 'break main')

p.interactive()
```

### Attach at Specific Address

```python
elf = ELF('./binary')

# Break at vulnerable function
vuln_addr = elf.symbols['vulnerable_function']

gdb_script = f'''
break *{hex(vuln_addr)}
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

p.sendline(b'input')
p.interactive()
```

## Debug with gdb.debug()

### Start with GDB

```python
# Start binary under GDB control
gdb.debug('./binary')

# GDB opens, binary paused at entry point
# Set breakpoints and continue
```

### Debug with Arguments

```python
# Pass arguments to binary
gdb.debug(['./binary', 'arg1', 'arg2'])

# Or with environment
gdb.debug('./binary', env={'VAR': 'value'})
```

### Debug with Script

```python
gdb_script = '''
break main
break vulnerable_function
continue
'''

gdb.debug('./binary', gdb_script)
```

## Exploit Debugging Workflow

### 1. Verify Offset with Cyclic Pattern

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Generate cyclic pattern
pattern = cyclic(200)

# Debug script to catch crash
gdb_script = '''
run
'''

p = gdb.debug('./binary', gdb_script)
p.sendline(pattern)
p.interactive()

# In GDB, when it crashes:
# info registers
# Find rip value (e.g., 0x61616161)
# Then: python3 -c "from pwn import *; print(cyclic_find(0x61616161))"
```

### 2. Verify Payload Before Sending

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Build payload
offset = 100
payload = b'A' * offset + p64(elf.symbols['win'])

# Debug before sending
gdb_script = '''
break vulnerable_function
continue
x/20x $rsp
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Inspect stack before sending
p.sendline(payload)
p.interactive()
```

### 3. Step Through ROP Chain Execution

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Build ROP chain
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])

# Debug ROP execution
gdb_script = '''
break main
continue
# Set breakpoint at first ROP gadget
break *0x400000
continue
# Step through gadgets
stepi
stepi
stepi
'''

p = process('./binary')
gdb.attach(p, gdb_script)

payload = b'A' * 100 + rop.chain()
p.sendline(payload)
p.interactive()
```

### 4. Inspect Memory During Exploitation

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Debug script to inspect memory
gdb_script = '''
break vulnerable_function
continue
# Print stack
x/20x $rsp
# Print registers
info registers
# Print specific memory
x/s 0x601234
# Continue
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

p.sendline(b'test')
p.interactive()
```

### 5. Verify Format String Offset

```python
from pwn import *

context(arch='amd64', os='linux')

# Debug format string
gdb_script = '''
break printf
continue
# Print registers and stack
info registers
x/20x $rsp
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send format string
p.sendline(b'%x.%x.%x.%x.%x.%x')
p.interactive()
```

### 6. Catch and Analyze Crashes

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Debug script to catch crash
gdb_script = '''
run
# When crash occurs, GDB will pause
# Inspect crash location
info registers
x/20x $rsp
backtrace
'''

p = gdb.debug('./binary', gdb_script)
p.sendline(b'A' * 1000)  # Trigger crash
p.interactive()
```

## GDB Commands Reference

### Breakpoints

```python
gdb_script = '''
# Break at function
break main
break vulnerable_function

# Break at address
break *0x400000

# Break at address with condition
break *0x400000 if $rax == 0x41414141

# Conditional breakpoint on function
break vulnerable_function if x > 100

# List breakpoints
info breakpoints

# Delete breakpoint
delete 1
'''
```

### Execution Control

```python
gdb_script = '''
# Run program
run

# Continue execution
continue

# Step into function
step

# Step over function
next

# Step one instruction
stepi

# Step over one instruction
nexti

# Finish current function
finish

# Jump to address
jump *0x400000
'''
```

### Inspection Commands

```python
gdb_script = '''
# Print registers
info registers

# Print specific register
print $rax
print $rsp

# Print memory (hex)
x/20x $rsp

# Print memory (string)
x/s 0x601234

# Print memory (instructions)
x/10i $rip

# Print variable
print variable_name

# Print array
print array[0]@10

# Backtrace
backtrace

# Print stack frame
info frame
'''
```

### Advanced Debugging

```python
gdb_script = '''
# Watch variable for changes
watch variable_name

# Print on breakpoint
commands 1
silent
print $rax
print $rsp
continue
end

# Conditional execution
if $rax == 0x41414141
  print "Found target value"
end

# Define custom command
define dump_stack
  x/20x $rsp
end

# Call custom command
dump_stack
'''
```

## Advanced Debugging Techniques

### 1. Breakpoint with Automatic Actions

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Break and automatically print values
gdb_script = '''
break vulnerable_function
commands 1
silent
print "=== Breakpoint Hit ==="
print $rax
print $rdi
print $rsi
x/20x $rsp
continue
end
run
'''

p = gdb.debug('./binary', gdb_script)
p.interactive()
```

### 2. Trace Execution with Logging

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Log execution trace
gdb_script = '''
set logging on
set logging file /tmp/gdb_trace.log
break main
continue
stepi
stepi
stepi
set logging off
'''

p = process('./binary')
gdb.attach(p, gdb_script)
p.interactive()

# Read trace
with open('/tmp/gdb_trace.log', 'r') as f:
    print(f.read())
```

### 3. Memory Watchpoint for Exploitation

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Watch specific memory location
target_addr = 0x601234
gdb_script = f'''
break main
continue
watch *{hex(target_addr)}
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send payload that modifies watched memory
payload = b'A' * 100 + p64(target_addr)
p.sendline(payload)
p.interactive()
```

### 4. Conditional Breakpoint for Offset Finding

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Break when specific value appears on stack
gdb_script = '''
break vulnerable_function
continue
# Break when rsp contains pattern
break *0x400000 if *(long*)$rsp == 0x61616161
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

pattern = cyclic(200)
p.sendline(pattern)
p.interactive()
```

### 5. Inspect ROP Gadget Execution

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')
rop = ROP(elf)

# Get first gadget address
rop.call('system', [next(elf.search(b'/bin/sh'))])
chain = rop.chain()

# Break at each gadget
gdb_script = '''
break main
continue
# Break at first gadget
break *0x400000
continue
# Step through gadgets
stepi
stepi
stepi
'''

p = process('./binary')
gdb.attach(p, gdb_script)

payload = b'A' * 100 + chain
p.sendline(payload)
p.interactive()
```

### 6. Verify Canary Bypass

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Debug canary location
gdb_script = '''
break vulnerable_function
continue
# Print stack to find canary
x/30x $rsp
# Set watchpoint on canary
watch *(long*)($rbp-8)
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send payload
p.sendline(b'A' * 100)
p.interactive()
```

## Terminal Configuration

### Set GDB Terminal

```python
# Use tmux (recommended for multiple windows)
context.terminal = ['tmux', 'new-window', '-n', 'gdb', '-c', '{cwd}']

# Use xterm
context.terminal = ['xterm', '-e']

# Use gnome-terminal
context.terminal = ['gnome-terminal', '--']

# Use screen
context.terminal = ['screen', '-X', 'screen', '-e', '^Aa']

# Now gdb.attach() will use configured terminal
p = process('./binary')
gdb.attach(p)
```

### Why Terminal Configuration Matters

- **tmux**: Best for scripting, allows multiple panes
- **xterm**: Simple, works everywhere
- **gnome-terminal**: GUI-friendly
- **screen**: Alternative to tmux

## Debugging Tips & Tricks

### 1. Quick Offset Finding

```python
from pwn import *

context(arch='amd64', os='linux')

# Use gdb.debug() to catch crash immediately
gdb_script = '''
run
# Crash will pause here
info registers
# Look at rip value
'''

p = gdb.debug('./binary', gdb_script)
p.sendline(cyclic(200))
p.interactive()

# In GDB: info registers
# Find rip value, then calculate offset
```

### 2. Print Stack Layout

```python
gdb_script = '''
break vulnerable_function
continue
# Print stack with addresses
x/30x $rsp
# Print in different formats
x/30gx $rsp  # 8-byte values
x/30wx $rsp  # 4-byte values
'''
```

### 3. Inspect Registers at Crash

```python
gdb_script = '''
run
# When crash occurs
info registers
# Print all registers
info all-registers
# Print specific register
print $rax
print $rbx
print $rcx
print $rdx
print $rsi
print $rdi
print $rbp
print $rsp
print $rip
'''
```

### 4. Follow Pointer Chain

```python
gdb_script = '''
break main
continue
# Print value at rsp
x/x $rsp
# Print value at that address
x/x 0x7ffffffde000
# Print value at that address
x/x 0x7ffffffde008
'''
```

### 5. Dump Binary Section

```python
gdb_script = '''
break main
continue
# Dump .text section
dump binary memory /tmp/text.bin 0x400000 0x401000
# Dump .data section
dump binary memory /tmp/data.bin 0x601000 0x602000
'''
```

### 6. Search Memory Pattern

```python
gdb_script = '''
break main
continue
# Search for pattern in memory
search 0x400000 0x500000 0x41414141
# Search for string
search 0x400000 0x500000 "/bin/sh"
'''
```

## Debugging Workflow Best Practices

### Step 1: Analyze Binary

```python
from pwn import *

context(arch='amd64', os='linux')
elf = ELF('./binary')

# Check protections
print(elf.checksec())

# List functions
print("Functions:", list(elf.symbols.keys())[:10])

# Find vulnerable function
if 'vulnerable' in elf.symbols:
    print(f"Vulnerable at: {hex(elf.symbols['vulnerable'])}")
```

### Step 2: Debug with Cyclic Pattern

```python
# Find offset using cyclic pattern
gdb_script = '''
run
# Crash will occur
info registers
# Note rip value
'''

p = gdb.debug('./binary', gdb_script)
p.sendline(cyclic(200))
p.interactive()
```

### Step 3: Verify Offset

```python
# Verify offset calculation
offset = cyclic_find(0x61616161)  # Replace with actual rip value
print(f"Offset: {offset}")

# Test with simple payload
payload = b'A' * offset + p64(0xdeadbeef)
p = process('./binary')
p.sendline(payload)
```

### Step 4: Build and Test Exploit

```python
# Build exploit with debugging
gdb_script = '''
break main
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send exploit
payload = b'A' * offset + p64(elf.symbols['win'])
p.sendline(payload)
p.interactive()
```

### Step 5: Verify Success

```python
# Test without GDB
p = process('./binary')
payload = b'A' * offset + p64(elf.symbols['win'])
p.sendline(payload)

# Check result
result = p.recvall()
print(result)
```

## Common Debugging Scenarios

### Scenario 1: Offset Finding Fails

```python
# Use GDB to find exact crash location
gdb_script = '''
run
# Crash occurs
info registers
# Print rip value
x/20x $rsp
# Print stack around crash
backtrace
# Print call stack
'''

p = gdb.debug('./binary', gdb_script)
p.sendline(cyclic(500))  # Increase size
p.interactive()
```

### Scenario 2: ROP Chain Not Working

```python
# Debug ROP execution
gdb_script = '''
break main
continue
# Set breakpoint at first gadget
break *0x400000
continue
# Step through gadgets
stepi
stepi
stepi
# Check registers after each step
info registers
'''

p = process('./binary')
gdb.attach(p, gdb_script)

rop = ROP(elf)
rop.call('system', [arg])
payload = b'A' * offset + rop.chain()
p.sendline(payload)
p.interactive()
```

### Scenario 3: Format String Offset Wrong

```python
# Debug format string
gdb_script = '''
break printf
continue
# Print stack
x/20x $rsp
# Print registers
info registers
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Test different offsets
for i in range(20):
    p.sendline(b'%' + str(i).encode() + b'$p')
    output = p.recvline()
    print(f"Offset {i}: {output}")
```

### Scenario 4: Canary Bypass Verification

```python
# Verify canary location and value
gdb_script = '''
break vulnerable_function
continue
# Print stack to find canary
x/30x $rsp
# Set watchpoint on canary
watch *(long*)($rbp-8)
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send payload that triggers canary check
p.sendline(b'A' * 100)
p.interactive()
```

## Limitations & Workarounds

- **GDB must be installed**: Install with `apt-get install gdb`
- **Terminal must be configured**: Set `context.terminal` appropriately
- **Stripped binaries**: Use `objdump` or `radare2` for symbol information
- **Slow on large binaries**: Use selective breakpoints
- **Remote debugging**: Use `gdb.attach()` with SSH tunneling

## Performance Tips

1. **Use selective breakpoints**: Only break where needed
2. **Avoid stepping through libraries**: Use `finish` to skip
3. **Cache binary analysis**: Load ELF once, reuse
4. **Use conditional breakpoints**: Reduce unnecessary stops
5. **Disable logging**: Only enable when needed

## Resources

- **GDB Documentation**: https://sourceware.org/gdb/documentation/
- **GDB Cheat Sheet**: https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf
- **Pwntools Docs**: https://docs.pwntools.com/

