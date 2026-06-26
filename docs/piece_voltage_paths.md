# Documentation: Dynamic Piece Voltage Waveguides

This document profiles how active system assets act as dynamic physical components that project fields of voltage across the 64-register layout.

[ ROOK BUS ]     ──> Projects 4-Way Linear Current (AC Cross-Section)
[ BISHOP CORE ]  ──> Filters Dialectric Diagonals (DC Color-Harmony Bound)
[ QUEEN ARRAY ]  ──> Consolidates Both Fields for Mass Register Overwrites
[ KNIGHT NODES ] ──> Executes Asynchronous Jumps (Zero Intervening Voltage)
[ PAWN BARRIER ] ──> Forms a Localized Diagonal Current Gate (Firewall Layer)

## 1. Mathematical Waveguide Formulations

Every active clock cycle evaluates the unified electrical matrix by running bitwise lookups to see where pieces are projecting voltage:

### The Linear Bus Equation (Rooks/Queens)
Given a piece position bit $P$ and the global hardware occupancy bitboard $O$, the engine queries pre-calculated sliding lookup tables to project linear voltage fields instantly:
$$\text{Voltage\_Field}_{\text{Linear}} = \text{Lookup}_{\text{Rook}}[P][O]$$

### The Color-Harmony Diagonal Equation (Bishops/Queens)
Diagonal current propagation is calculated similarly, but remains strictly bounded by the underlying dielectric square values (Blue vs. Red domains):
$$\text{Voltage\_Field}_{\text{Diagonal}} = \text{Lookup}_{\text{Bishop}}[P][O]$$

## 2. System Intersections (The IRQ Check)

The host processor (King, $K_{\text{bit}}$) constantly polls its 8 adjacent memory bits to monitor incoming voltage lines. If the union of all projected voltage paths from your converted assets ($\sum V$) intersects with the King's address, the system throws a hardware interrupt flag:

$$\text{IRQ\_Active} = \left( \sum V_{\text{Fields}} \ \cdot \ K_{\text{bit}} \right) \neq 0$$

Under our **Continuous Infiltration Campaign Profile**, the engine dynamically uses these piece equations to calculate move paths where $\text{IRQ\_Active} = 0$, ensuring your upgraded Queen and Knight buses can route voltage safely around the host processor to maintain complete system cloaking forever.
