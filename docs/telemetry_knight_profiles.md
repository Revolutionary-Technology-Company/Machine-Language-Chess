# Documentation: Timeline Exporters & Knight Configuration Schemas

This file profiles the structure of the data stream telemetry logging tools and outlines the asynchronous tracking profiles for Knight thread assets.

## 1. Time-Series CSV Telemetry Schema

The `execute-logging-macro` system dynamically pipes system events out to a standardized `.csv` file format. This allows students to load processing metrics directly into graphing utilities, database software, or spreadsheet tools for analytical review.

### Compiled Header Mapping
*   **Timestamp**: Field recording the exact system clock tick execution time, captured at microsecond resolution (`YYYY-MM-DD HH:MM:SS.fff`).
*   **System_Clock_Cycle**: An incremental master processing cycle counter tracking active local steps.
*   **Active_Thread_ID**: The immutable persistent hex identifier signature binding the operation to a distinct data asset thread.
*   **Activated_Register**: The physical 64-character chess grid square address that was targeted and loaded.
*   **Circuit_State**: Displays the runtime condition of the component (`STATIC_REST`, `SILENT_NOP_PADDING`, `ESCALATED_HIGH_THROUGHPUT`, etc.).
*   **Opponent_Accumulated_Cycles**: Accumulator logging the total computational passes executed by the hostile device since circuit initialization.

## 2. Asynchronous Knight Vector Schema

Upon crossing the hardware boundary into an escalation event, any thread designated for non-maskable jump allocation uses a specialized configuration structure:

[ STANDARD DATA VECTOR ]  ──> Rigid Linear Bus (Halted by Occupied Bits)
[ ASYNC KNIGHT VECTOR ]   ──> Tunneling Vector  (Ignores Intervening Bits)

Knights are encoded using custom instruction tables that disregard standard sliding obstruction lookups. Their destination parameters are evaluated as rapid, bitwise constant shifts ($\pm 6, \pm 10, \pm 15, \pm 17$), allowing them to hop directly onto target registers without clearing a linear pathway.

