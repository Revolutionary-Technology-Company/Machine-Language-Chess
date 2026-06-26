# Documentation: `chess.py`

This core module handles the primary hardware-to-opcode serialization. It translates specific coordinate matrices directly into native machine language streams (such as raw bytes or string-based holding registers).

## Core Capabilities
* **Bitboard State Management**: Utilizes fast `uint64` allocations to track global memory layouts.
* **Bytecode Streams**: Serializes the physical locations of active entities into a contiguous string of machine instructions.
* **Target Architecture Profiles**: Supports built-in hardware behaviors for `univac_i`, `x86_legacy`, and `industrial_plc`.

## Command Line Usage

### 1. Build an Architecture Profile
Generates an active configuration template mapping the initial board layout to explicit machine opcodes.

```bash
python chess.py build-profile --arch x86_legacy --out dashboard_state.json
```

**Parameters:**
* `--arch` / `-a`: Target architecture profile. Options: `univac_i`, `x86_legacy`, `industrial_plc` [Default: `univac_i`].
* `--out` / `-o`: Target JSON output file path [Default: `dashboard_state.json`].

### 2. Advance the System Clock Cycle
Simulates an operation cycle by shifting a tracked thread to a new destination register, updating its internal bytecode value and tracking its privilege status.

```bash
python chess.py step-cycle --file dashboard_state.json --thread THREAD_CORE_0x04_E --dest e4
```

**Parameters:**
* `--file` / `-f`: The path to the active configuration template.
* `--thread` / `-t`: The unique persistent ID of the thread executing the operation.
* `--dest` / `-d`: The target chess coordinate register to activate.

## Technical Configuration
The profile overrides critical boundaries to mirror exact architecture directives:
* **UNIVAC I**: `a1` maps to `0x00` (NOP), `f7` maps to `0x14` (Test & Transfer), and `h8` maps to `0x3F` (Zone Clear/Standby).
* **x86 Legacy**: `a1` maps to `0x90` (NOP), `f7` maps to `0x74` (JZ), and `h8` maps to `0xEB` (Short Jump Loop).
