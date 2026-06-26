# Documentation: Square Voltage Systems and Capture Gates

This file details the electrical matrix layout mapping and asset collision mathematics enforced by the engine pipeline.

## 1. Square Voltage System (Your Formulation)

To evaluate energy paths natively, the system translates piece placement and coordinate colors into a 1-bit binary voltage state:
*   **Voltage State: 0**: Occurs when an asset is positioned on an address corresponding to a physical White square. Mapped visually to **Blue** terminal space.
*   **Voltage State: 1**: Occurs when an asset is positioned on an address corresponding to a physical Black square. Mapped visually to **Red** terminal space.

### Live Logic Matrix
[White Piece] on [White Square] ──> Logic Output: 0 (Low Voltage / Blue)
[White Piece] on [Black Square] ──> Logic Output: 1 (High Voltage / Red)
[Black Piece] on [Black Square] ──> Logic Output: 1 (High Voltage / Red)
[Black Piece] on [White Square] ──> Logic Output: 0 (Low Voltage / Blue)

## 2. Collision Processing (The Piece Capture Gate)

When a local thread attempts to migrate to an address index already populated by an opposing system variable, the transaction resolves through a hardware combinational circuit.

### Gate Inputs
*   **$L$ (Local Active)**: A local thread asserts a write command to the address block.
*   **$H$ (Hostile Active)**: A pre-existing host variable occupies the target register block.
*   **$R$ (Risk-Index Pass)**: The target variable matches the highest-priority threat requirement calculated by our threat matrix.

### System Equations
1.  **Capture Action ($C$)**: Determines if an explicit delete operation is calculated:
    $$C = L \cdot H \cdot R$$
2.  **Write Enable ($Y$)**: Determines if the overall space migration is legally permitted by the system bus:
    $$Y = (L \cdot \bar{H}) + (L \cdot H \cdot R)$$

If a local thread encounters an unlisted or low-risk hostile asset ($R = 0$), the write operation evaluates to a global `0`. The instruction is safely dropped from the execution pipeline, preserving your local thread integrity.
