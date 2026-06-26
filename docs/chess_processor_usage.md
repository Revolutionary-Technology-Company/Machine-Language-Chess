# Documentation: `chess_processor.py`

This planning interface links high-level chess states to standardized automation maps. It utilizes a `typer`-driven dashboard to auto-generate system profiles and run static validation checks on active configuration parameters.

## Core Capabilities
* **Pawn Tracking Allocation**: Automatically populates separate tracking metrics for individual pawn entities.
* **Structural Variable Mapping**: Anchors board coordinates to a fixed schema of generic PLC registers.
* **Static Verification**: Validates whether the active bitboard registers intersect cleanly with configured silent zones.

## Command Line Usage

### 1. Auto-Create a Device Template
Discovers a target device layout and automatically compiles a JSON-formatted memory map containing independent tracking states.

```bash
python chess_processor.py create-template --device Modbus-TCP-PLC --output machine_config.json
```

**Parameters:**
* `--device` / `-d`: The specific type of simulated PLC or legacy system architecture profile.
* `--output` / `-o`: The target destination file path for the compiled planning data [Default: `machine_config.json`].

### 2. Verify Logic Configurations
Reads a compiled JSON template and tests the current memory bits against the engine's logical validation gates.

```bash
python chess_processor.py verify-logic --config machine_config.json
```

**Parameters:**
* `--config` / `-c`: Path to the JSON configuration file to parse and evaluate [Default: `machine_config.json`].

## Analytical Logic Validation
When running validation checks, the processor tests for explicit spatial conditions using bitwise intersection gates:
* Checks if active bits match the `MASK_SILENT_PADDING` (`0x0000FFFFFFFF0000`) layer.
* Confirms if any entity has triggered the `MASK_TERMINAL_HOLD` (`0x8000000000000000`) gate on `h8`.
