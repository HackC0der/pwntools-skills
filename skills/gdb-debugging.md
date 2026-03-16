# Pwntools GDB: Debugging Integration

## Overview

Pwntools integrates with GDB for debugging binaries during exploitation. Use `gdb.attach()` to attach to running processes or `gdb.debug()` to start with GDB.

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

### Attach with Script

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

### Attach with Breakpoint

```python
elf = ELF('./binary')

p = process('./binary')

# Attach and break at main
gdb.attach(p, 'break main')

p.interactive()
```

## Debug with GDB

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

## GDB Scripts

### Common GDB Commands

```python
gdb_script = '''
# Set breakpoints
break main
break 0x400000

# Set conditional breakpoint
break vulnerable_function if x > 100

# Continue execution
continue

# Step into function
step

# Step over function
next

# Print variable
print x
print $rax

# Print memory
x/100x $rsp

# Print registers
info registers

# Backtrace
backtrace
'''

p = process('./binary')
gdb.attach(p, gdb_script)
```

### Inspect Memory

```python
gdb_script = '''
# Break at function
break vulnerable_function

# Continue to breakpoint
continue

# Print stack
x/20x $rsp

# Print heap
x/20x $rax

# Print string
x/s 0x601234
'''

p = process('./binary')
gdb.attach(p, gdb_script)
```

## Common Patterns

### Debug Buffer Overflow

```python
elf = ELF('./binary')

gdb_script = '''
break vulnerable_function
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send payload
payload = cyclic(200)
p.sendline(payload)

p.interactive()
```

### Debug Format String

```python
gdb_script = '''
break printf
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send format string
p.sendline(b'%x.%x.%x.%x')

p.interactive()
```

### Debug ROP Chain

```python
elf = ELF('./binary')
rop = ROP(elf)

gdb_script = '''
break main
continue
'''

p = process('./binary')
gdb.attach(p, gdb_script)

# Send ROP payload
payload = b'A' * 100 + rop.chain()
p.sendline(payload)

p.interactive()
```

## Terminal Configuration

### Set GDB Terminal

```python
# Use tmux
context.terminal = ['tmux', 'new-window', '-n', 'gdb', '-c', '{cwd}']

# Use xterm
context.terminal = ['xterm', '-e']

# Use gnome-terminal
context.terminal = ['gnome-terminal', '--']

# Now gdb.attach() will use configured terminal
p = process('./binary')
gdb.attach(p)
```

## Debugging Tips

### Inspect Registers

```python
gdb_script = '''
break main
continue
info registers
'''

p = process('./binary')
gdb.attach(p, gdb_script)
```

### Inspect Stack

```python
gdb_script = '''
break vulnerable_function
continue
x/20x $rsp
'''

p = process('./binary')
gdb.attach(p, gdb_script)
```

### Inspect Heap

```python
gdb_script = '''
break malloc
continue
x/20x $rax
'''

p = process('./binary')
gdb.attach(p, gdb_script)
```

## Limitations

- GDB must be installed
- Terminal must be configured for interactive use
- Some operations may be slow with large binaries
- Breakpoints may not work on stripped binaries
