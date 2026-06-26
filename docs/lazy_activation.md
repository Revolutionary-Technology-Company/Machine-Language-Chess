# Documentation: Lazy Activation & The Immutable Rest State

This module establishes the laws of resource conservation within the chess matrix pipeline. An asset that does not move does not compute.

## 1. The Immutable Rest State (`STATIC_REST`)

In standard computing, spinning up continuous loops to monitor variables that haven't changed wastes immense processing power. To maximize efficiency, our chess engine enforces an **Immutable Rest State**:
*   While a piece sits unmoved on its original register address, its electrical output is coded as a hard `0`.
*   It does not broadcast a attack vector, it does not calculate sliding lookup matrices, and it causes zero systemic changes to the background environment.
*   It exists purely as a static allocation of memory bits (data at rest).

## 2. Closing the Circuit (`DYNAMIC_CURRENT`)

The instant a user triggers a clock cycle and moves a piece, the system architecture executes an immediate state transition:

[ UNMOVED PIECE ] ──> Circuit Open ──> Status: STATIC_REST    (0 Volts / No Change)
[ EXECUTED MOVE ] ──> Circuit Closed ──> Status: DYNAMIC_CURRENT (Dynamic Bus Active)

Upon physical migration across the grid:
1.  The asset's properties flip instantly to `DYNAMIC_CURRENT`.
2.  The engine passes its new bit location down the **NJIT FastMath lookups** to project active linear or diagonal voltage paths across the board.
3.  The asset officially interacts with the host infrastructure, allowing the planning dashboard to calculate risk assessments and predictive trajectory models based only on components that are actively running.
