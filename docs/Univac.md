The UNIVAC-Chess Mapping Matrix

On a UNIVAC system, 1-byte commands are read directly by the Control Unit. Here is how your pieces navigate the board squares to execute explicit system commands, ensuring no move is "random noise":

```
  [FILE A]   [FILE B]   [FILE C]   [FILE D]   [FILE E]   [FILE F]   [FILE G]   [FILE H]
  (UNIVAC)   (UNIVAC)   (UNIVAC)   (UNIVAC)   (UNIVAC)   (UNIVAC)   (UNIVAC)   (UNIVAC)
 RANK 8 |    A     |    B     |    C     |    D     |    E     |    F     |    G     |    H     |
 RANK 7 |    I     |    J     |    K     |    L     |    M     |    N     |    O     |    P     |
 RANK 6 |    Q     |    R     |    S     |    T     |    U     |    V     |    W     |    X     |
 RANK 5 |    Y     |    Z     |    0     |    1     |    2     |    3     |    4     |    5     |
 RANK 4 |    6     |    7     |    8     |    9     |    .     |    ,     |    -     |    /     |
 RANK 3 | [Space]  |    (     |    )     |    $     |    *     |    %     |    =     |    +     |
 RANK 2 |  [0x08]  |  [0x09]  |  [0x0A]  |  [0x0B]  |  [0x0C]  |  [0x0D]  |  [0x0E]  |  [0x0F]  |
 RANK 1 |  [0x00]  |  [0x01]  |  [0x02]  |  [0x03]  |  [0x04]  |  [0x05]  |  [0x06]  |  [0x07]  |

```

* * * * *

The Exploitation Script: Moving Only to Activate/Deactivate

To achieve remote control without triggering a system halt (avoiding the enemy King), your army must strictly execute the following three operational movesets:

Phase 1: Overwriting the Input Buffer (Setting up the Exploitation)

To start taking over, your pawns move into **Rank 5** and **Rank 6**. You are explicitly landing on squares that allow you to read and write memory registers without authorization.

-   **Move to Square c6 (`S` Command - Shift Right):** This command shifts data in the internal registers. By landing a piece here, you manually shift the system's security tokens out of the way, creating a memory gap.
-   **Move to Square d6 (`T` Command - Test and Transfer):** This is a conditional jump. Moving a piece here tests whether your infiltration thread has successfully bypassed the firewall. If it returns `True`, the script transfers control directly to your payload.

Phase 2: Allocating Remote Control Memory (Activating the High-Power Tokens)

When your pawns reach **Rank 8**, they trigger privilege escalation. You explicitly target squares mapped to the UNIVAC's core memory transfer opcodes, effectively installing your "remote control shell."

-   **Promote on Square a8 (`A` Command - Add / Load Memory):** This instruction loads data directly into the system's primary accumulator. By promoting to a Queen here, you overwrite the memory sector, forcing the CPU to read your Queen's movement coordinates as the next system instructions.
-   **Promote on Square c8 (`C` Command - Clear and Add):** Clears the previous, legitimate instructions of the host system and substitutes them entirely with your malicious logic.

Phase 3: The Infinite Loop Cloaking Routine (Deactivating the Termination Flags)

As your pieces move around the board, the enemy King will try to step into their attack vectors, which would cause an automatic checkmate (`HLT`) and kill your connection. Your script must actively *deactivate* the King's ability to trigger a halt by forcing him into a **Non-Terminating Standby Loop**.

-   **Move to Rank 4 (`.` and `,` Commands - Skip/Ignore):** In the UNIVAC architecture, these characters can act as punctuation or ignorable shifts. By moving your defensive pieces exclusively through **Rank 4**, you are executing "No-Operation" (`NOP`) pad bytes.
-   **The Result:** You fill the execution timeline with empty space. The enemy King is forced to constantly step into these empty `NOP` slots. He stays alive, moving endlessly on useless cycles, while your promoted Queens and Knights on the upper ranks have total, unhindered remote control over the rest of the processor's resources.
