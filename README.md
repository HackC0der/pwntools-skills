# Pwntools Skills Guide

[中文版本](#中文版本) | [English Version](#english-version)

---

## English Version

### Overview

**Pwntools Skills** is a comprehensive guide for using [pwntools](https://github.com/Gallopsled/pwntools) in CTF (Capture The Flag) competitions and binary exploitation. This skill provides structured documentation, practical examples, and best practices for binary exploitation, ROP chains, shellcode generation, format string exploitation, and more.

### Quick Start

```python
from pwn import *

# Configure context
context(arch='amd64', os='linux')

# Start process
p = process('./binary')

# Send and receive
p.sendline(b'input')
data = p.recv(1024)

# Interactive mode
p.interactive()
```

### What's Included

#### 📚 Skill Modules (11 files)
- **Tubes Communication** - Process/socket/SSH interaction
- **ELF Binary Analysis** - Binary parsing and symbol resolution
- **Packing Utilities** - Byte packing/unpacking
- **Shellcraft** - Shellcode generation
- **Cyclic Patterns** - Offset finding with cyclic patterns
- **ROP Exploitation** - ROP chain building
- **Format Strings** - Format string vulnerability exploitation
- **Context Configuration** - Global settings
- **Assembly/Disassembly** - Code generation and analysis
- **GDB Debugging** - Debugging integration
- **DynELF** - Runtime libc symbol resolution

#### 📖 Reference Documentation
- **modules-overview.md** - Complete module hierarchy and relationships
- **best-practices.md** - Development workflow and code organization
- **troubleshooting.md** - Common issues and solutions

#### 💻 Practical Examples
- **buffer-overflow.py** - Basic buffer overflow exploitation
- **rop-chain.py** - ROP chain building and execution
- **format-string.py** - Format string exploitation
- **shellcode.py** - Shellcode generation and injection

### Common Exploitation Patterns

#### Buffer Overflow with ROP
```python
# 1. Find offset
pattern = cyclic(200)
offset = cyclic_find(crash_addr)

# 2. Build ROP chain
elf = ELF('./binary')
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])

# 3. Send payload
payload = b'A' * offset + rop.chain()
p.sendline(payload)
```

#### Format String Exploitation
```python
# 1. Find offset (automated)
def exec_fmt(payload):
    p = process('./binary')
    p.sendline(payload)
    return p.recvall()

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

# 2. Write memory
payload = fmtstr_payload(offset, {target_addr: value})
p.sendline(payload)
```

#### Shellcode Injection
```python
# 1. Generate shellcode
context(arch='amd64', os='linux')
shellcode = asm(shellcraft.sh())

# 2. Inject and execute
payload = b'A' * offset + shellcode
p.sendline(payload)
```

### Architecture Support

Pwntools supports multiple architectures:
- **x86**: amd64, i386
- **ARM**: arm, thumb, aarch64
- **MIPS**: mips, mips64
- **PowerPC**: ppc, ppc64
- **SPARC**: sparc, sparc64
- **RISC-V**: riscv64

### Best Practices

1. **Always set context first**: `context(arch='amd64', os='linux')`
2. **Use cyclic patterns for offset finding**: More reliable than manual counting
3. **Enable logging during development**: `context.log_level = 'debug'`
4. **Test locally before remote**: Verify exploit works on local binary
5. **Handle timeouts gracefully**: Set appropriate timeout values
6. **Use context managers**: `with process('./binary') as p:` for auto-cleanup
7. **Verify protections**: Use `elf.checksec()` to understand mitigations

### File Structure

```
pwntools-skills/
├── SKILL.md                    # Main skill file
├── README.md                   # This file
├── reference/
│   ├── modules-overview.md     # Module reference
│   ├── best-practices.md       # Best practices
│   └── troubleshooting.md      # Troubleshooting guide
├── skills/
│   ├── tubes-communication.md
│   ├── elf-binary-analysis.md
│   ├── rop-exploitation.md
│   ├── format-string-exploitation.md
│   └── ... (7 more skill modules)
└── examples/
    ├── buffer-overflow.py
    ├── rop-chain.py
    ├── format-string.py
    └── shellcode.py
```

### Resources

- **Official Docs**: https://docs.pwntools.com/
- **GitHub**: https://github.com/Gallopsled/pwntools
- **Tutorials**: https://github.com/Gallopsled/pwntools-tutorial
- **Write-ups**: https://github.com/Gallopsled/pwntools-write-ups
- **Discord**: https://discord.gg/96VA2zvjCB

### When to Use This Skill

Use this skill when:
- Working on binary exploitation challenges (CTF, pwn)
- Building ROP chains or shellcode
- Analyzing ELF binaries
- Exploiting format string vulnerabilities
- Bypassing protections (ASLR, DEP, canaries)
- Debugging exploitation code with GDB
- Generating payloads for buffer overflows

### License

MIT License - See LICENSE file for details

---

## 中文版本

### 概述

**Pwntools 技能指南**是一份关于在 CTF（夺旗竞赛）和二进制利用中使用 [pwntools](https://github.com/Gallopsled/pwntools) 的综合指南。本技能提供结构化文档、实践示例和最佳实践，涵盖二进制利用、ROP 链、Shellcode 生成、格式字符串利用等内容。

### 快速开始

```python
from pwn import *

# 配置上下文
context(arch='amd64', os='linux')

# 启动进程
p = process('./binary')

# 发送和接收
p.sendline(b'input')
data = p.recv(1024)

# 交互模式
p.interactive()
```

### 包含内容

#### 📚 技能模块（11 个文件）
- **Tubes 通信** - 进程/套接字/SSH 交互
- **ELF 二进制分析** - 二进制解析和符号解析
- **打包工具** - 字节打包/解包
- **Shellcraft** - Shellcode 生成
- **循环模式** - 使用循环模式查找偏移
- **ROP 利用** - ROP 链构建
- **格式字符串** - 格式字符串漏洞利用
- **上下文配置** - 全局设置
- **汇编/反汇编** - 代码生成和分析
- **GDB 调试** - 调试集成
- **DynELF** - 运行时 libc 符号解析

#### 📖 参考文档
- **modules-overview.md** - 完整的模块层级和关系
- **best-practices.md** - 开发工作流和代码组织
- **troubleshooting.md** - 常见问题和解决方案

#### 💻 实践示例
- **buffer-overflow.py** - 基础缓冲区溢出利用
- **rop-chain.py** - ROP 链构建和执行
- **format-string.py** - 格式字符串利用
- **shellcode.py** - Shellcode 生成和注入

### 常见利用模式

#### 缓冲区溢出 + ROP
```python
# 1. 查找偏移
pattern = cyclic(200)
offset = cyclic_find(crash_addr)

# 2. 构建 ROP 链
elf = ELF('./binary')
rop = ROP(elf)
rop.call('system', [next(elf.search(b'/bin/sh'))])

# 3. 发送负载
payload = b'A' * offset + rop.chain()
p.sendline(payload)
```

#### 格式字符串利用
```python
# 1. 查找偏移（自动化）
def exec_fmt(payload):
    p = process('./binary')
    p.sendline(payload)
    return p.recvall()

autofmt = FmtStr(exec_fmt)
offset = autofmt.offset

# 2. 写入内存
payload = fmtstr_payload(offset, {target_addr: value})
p.sendline(payload)
```

#### Shellcode 注入
```python
# 1. 生成 shellcode
context(arch='amd64', os='linux')
shellcode = asm(shellcraft.sh())

# 2. 注入并执行
payload = b'A' * offset + shellcode
p.sendline(payload)
```

### 架构支持

Pwntools 支持多种架构：
- **x86**: amd64, i386
- **ARM**: arm, thumb, aarch64
- **MIPS**: mips, mips64
- **PowerPC**: ppc, ppc64
- **SPARC**: sparc, sparc64
- **RISC-V**: riscv64

### 最佳实践

1. **始终先设置上下文**: `context(arch='amd64', os='linux')`
2. **使用循环模式查找偏移**: 比手动计数更可靠
3. **开发时启用日志**: `context.log_level = 'debug'`
4. **本地测试后再远程测试**: 验证利用在本地二进制上有效
5. **优雅处理超时**: 设置适当的超时值
6. **使用上下文管理器**: `with process('./binary') as p:` 自动清理
7. **验证保护机制**: 使用 `elf.checksec()` 了解防护措施

### 文件结构

```
pwntools-skills/
├── SKILL.md                    # 主技能文件
├── README.md                   # 本文件
├── reference/
│   ├── modules-overview.md     # 模块参考
│   ├── best-practices.md       # 最佳实践
│   └── troubleshooting.md      # 故障排除指南
├── skills/
│   ├── tubes-communication.md
│   ├── elf-binary-analysis.md
│   ├── rop-exploitation.md
│   ├── format-string-exploitation.md
│   └── ... (7 个其他技能模块)
└── examples/
    ├── buffer-overflow.py
    ├── rop-chain.py
    ├── format-string.py
    └── shellcode.py
```

### 资源

- **官方文档**: https://docs.pwntools.com/
- **GitHub**: https://github.com/Gallopsled/pwntools
- **教程**: https://github.com/Gallopsled/pwntools-tutorial
- **Write-ups**: https://github.com/Gallopsled/pwntools-write-ups
- **Discord**: https://discord.gg/96VA2zvjCB

### 何时使用本技能

在以下情况下使用本技能：
- 参与二进制利用挑战（CTF、pwn）
- 构建 ROP 链或 Shellcode
- 分析 ELF 二进制文件
- 利用格式字符串漏洞
- 绕过保护机制（ASLR、DEP、栈金丝雀）
- 使用 GDB 调试利用代码
- 为缓冲区溢出生成负载

### 许可证

MIT 许可证 - 详见 LICENSE 文件

---

### 贡献

欢迎提交 Issue 和 Pull Request！

### 联系方式

- GitHub: https://github.com/HackC0der/pwntools-skills
- Issues: https://github.com/HackC0der/pwntools-skills/issues
