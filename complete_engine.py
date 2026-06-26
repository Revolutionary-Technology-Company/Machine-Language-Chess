import sys
import json
import numpy as np
import typer
from typing import Dict, List, Optional

# Initialize the Typer CLI app context
app = typer.Typer(help="🚀 ULTIMATE CHESS-TO-MACHINE ARCHITECTURE DASHBOARD 🚀")

# ==========================================
# 1. THE COMPLETE FASTMATH BITBOARD MATRIX
# ==========================================
# Every square on the 8x8 grid mapped to its exact bit position index (0 to 63)
SQUARES = {
    f"{chr(97+f)}{r+1}": (r * 8) + f for r in range(8) for f in range(8)
}

# Pre-compiled High-Performance Logic Masks
MASK_RANK_1_2 = np.uint64(0x000000000000FFFF)  # Base Gateway Input Buffer
MASK_RANK_3_4 = np.uint64(0x0000FFFFFFFF0000)  # Ultra-Silent Padding / NOP Zone
MASK_RANK_7_8 = np.uint64(0xFFFF000000000000)  # Privilege Escalation Domain
MASK_SQUARE_H8 = np.uint64(1  Dict:
        """Flushes the current runtime metrics into a unified layout dictionary."""
        return {
            "System_Architecture_Profile": self.profile_name,
            "Description": self.profile["description"],
            "Global_Memory_Bitboard": hex(self.system_bitboard),
            "Flags": {
                "Silent_Zone_Occupied": bool((self.system_bitboard & MASK_RANK_3_4) != 0),
                "Escalation_Zone_Active": bool((self.system_bitboard & MASK_RANK_7_8) != 0),
                "Infinite_Loop_Locked": bool((self.system_bitboard & MASK_SQUARE_H8) != 0)
            },
            "Active_Core_Threads": self.thread_registry
        }
MASK_SILENT_PADDING = np.uint64(0x0000FFFFFFFF0000) # Ranks 3-4: Safe Standby Zones

# Global Alphanumeric Coordinate to Bit Index Map
SQUARES = {f"{chr(97+f)}{r+1}": (r * 8) + f for r in range(8) for f in range(8)}
INDEX_TO_SQUARE = {v: k for k, v in SQUARES.items()}

# NJIT FastMath: Standard bitmask identifying all 32 Black squares on a board
MASK_BLACK_SQUARES = np.uint64(0xAA55AA55AA55AA55)

def calculate_square_voltage(piece_mask: np.uint64, is_black_piece: bool) -> int:
    """Implements your exact color-matching boolean rule natively."""
    is_on_black_square = (piece_mask & MASK_BLACK_SQUARES) != 0
    
    if not is_black_piece:  # White Piece
        return 1 if is_on_black_square else 0
    else:                   # Black Piece
        return 1 if is_on_black_square else 0

class AdvancedSystemBridge:
    def __init__(self, profile_name: str):
        self.profile_name = profile_name
        self.system_bitboard = np.uint64(0)
        self.thread_registry: Dict[str, Dict] = {}
        
        # Simulated Host Core Registers (The Opponent)
        self.enemy_king_bit = np.uint64(1  int:
        """Counts how many local threads have achieved privilege escalation."""
        return sum(1 for t in self.thread_registry.values() if t["privilege_level"] == "ROOT_SYSTEM_QUEEN")

    def simulate_king_legal_branches(self, current_king_bit: np.uint64) -> List[np.uint64]:
        """Calculates all possible adjacent physical memory addresses the King could step to."""
        king_idx = int(np.log2(float(current_king_bit)))
        rank = king_idx // 8
        file = king_idx % 8
        branches = []
        
        # 8-Way directional vector check
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0:
                    continue
                nr, nf = rank + dr, file + df
                if 0 <= nr < 8 and 0 <= nf < 8:
                    target_idx = (nr * 8) + nf
                    branches.append(np.uint64(1 << target_idx))
        return branches

    def predict_optimal_steering_vector(self, favorable_target_coord: str) -> Optional[str]:
        """
        Predictive Trajectory Matrix: Analyzes the host CPU's available escape branches 
        and selects the move that most efficiently forces him toward the target register.
        """
        target_bit = np.uint64(1 << SQUARES[favorable_target_coord.lower()])
        target_idx = SQUARES[favorable_target_coord.lower()]
        
        current_king_idx = int(np.log2(float(self.enemy_king_bit)))
        possible_escapes = self.simulate_king_legal_branches(self.enemy_king_bit)
        
        promotion_count = self.get_total_promotions()
        
        # PHASE 1: Throttling Phase - Infiltration is incomplete
        if promotion_count < 8:
            return f"[PHASE 1: INFILTRATION] Strategy Locked: Advancing remaining {8 - promotion_count} threads to Rank 8 first."
            
        # PHASE 2: Extraction Phase - All 8 Queens are online. Begin predictive steering.
        best_escape_bit = None
        min_distance = float('inf')
        
        # Calculate geometric and register distance vector to target
        target_r, target_f = target_idx // 8, target_idx % 8
        
        for escape_bit in possible_escapes:
            escape_idx = int(np.log2(float(escape_bit)))
            esc_r, esc_f = escape_idx // 8, escape_idx % 8
            
            # Distance computation (Chebyshev distance for chess matrix)
            distance = max(abs(esc_r - target_r), abs(esc_f - target_f))
            
            if distance < min_distance:
                min_distance = distance
                best_escape_bit = escape_bit
                
        if best_escape_bit is not None:
            next_sq_name = INDEX_TO_SQUARE[int(np.log2(float(best_escape_bit)))]
            return f"[PHASE 2: EXTRACTION] To guide King to {favorable_target_coord.upper()}, cut off all pathways except register: {next_sq_name.upper()}"
        
        return "System Standby: Target register optimization locked."

    def execute_clock_cycle(self, thread_id: str, destination_coord: str) -> bool:
        """Processes a single thread shift and updates privilege tiers dynamically."""
        if thread_id not in self.thread_registry:
            return False
        thread = self.thread_registry[thread_id]
        old_mask = np.uint64(1 << SQUARES[thread["current_coordinate"]])
        new_mask = np.uint64(1 << SQUARES[destination_coord])
        
        self.system_bitboard &= ~old_mask
        self.system_bitboard |= new_mask
        thread["current_coordinate"] = destination_coord
        
        if (new_mask & MASK_RANK_7_8) != 0:
            thread["privilege_level"] = "ROOT_SYSTEM_QUEEN"
            thread["execution_state"] = "ESCALATED_HIGH_THROUGHPUT"
        return True

    def compile_dashboard_state(self) -> Dict:
        return {
            "Global_Memory_Bitboard": hex(self.system_bitboard),
            "Host_King_Register": INDEX_TO_SQUARE[int(np.log2(float(self.enemy_king_bit)))].upper(),
            "Total_Escalated_Threads": f"{self.get_total_promotions()}/8",
            "Active_Core_Threads": self.thread_registry
        }

# ==========================================
# 4. TYPER CLI DASHBOARD COMMAND INTERFACE
# ==========================================
@app.command()
def build_profile(
    architecture: str = typer.Option("univac_i", "--arch", "-a", help="Select hardware core profile: univac_i, x86_legacy, industrial_plc"),
    output: str = typer.Option("dashboard_blueprint.json", "--out", "-o", help="File target to export the runnable architecture state")
):
    """
    Constructs an interactive hardware emulation layout, registers all threads independently, 
    and saves a complete runnable mapping file.
    """
    typer.secho(f"🚀 Initializing System Compiler Profile: {architecture.upper()}", fg=typer.colors.CYAN, bold=True)
    
    bridge = AdvancedSystemBridge(architecture)
    bridge.allocate_independent_threads()
    
    state_blueprint = bridge.compile_dashboard_state()
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(state_blueprint, f, indent=4)
        
    typer.secho(f"✨ Success! Compiled blueprint written to -> {output}", fg=typer.colors.GREEN)
    typer.echo("[📊 STATUS]: Thread registries mapped. Core execution loop ready.")

@app.command()
def step_cycle(
    blueprint_file: str = typer.Option("dashboard_blueprint.json", "--file", "-f", help="Target blueprint file to modify"),
    thread: str = typer.Option(..., "--thread", "-t", help="The specific entity ID to shift (e.g., THREAD_CORE_0x04_E)"),
    destination: str = typer.Option(..., "--dest", "-d", help="Target chess square register coordinate to activate (e.g., e4)")
):
    """
    Executes a single hardware clock cycle. Moves a tracked thread to a new board space, 
    translates its opcode, re-evaluates its privilege tier, and overwrites the blueprint.
    """
    try:
        with open(blueprint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        arch = data["System_Architecture_Profile"]
        bridge = AdvancedSystemBridge(arch)
        bridge.system_bitboard = np.uint64(int(data["Global_Memory_Bitboard"], 16))
        bridge.thread_registry = data["Active_Core_Threads"]
        
        typer.echo(f"🔄 Advancing master clock loop for {arch}...")
        if bridge.execute_clock_cycle(thread, destination.lower()):
            updated_blueprint = bridge.compile_dashboard_state()
            
            with open(blueprint_file, 'w', encoding='utf-8') as f:
                json.dump(updated_blueprint, f, indent=4)
                
            typer.secho(f"✅ Cycle Committed! Thread {thread} migrated to register {destination.upper()}.", fg=typer.colors.GREEN)
            typer.echo(f" New State: {updated_blueprint['Active_Core_Threads'][thread]['execution_state']}")
            typer.echo(f" Privilege: {updated_blueprint['Active_Core_Threads'][thread]['privilege_level']}")
        else:
            typer.secho(f"❌ Error: Thread ID '{thread}' not found in runtime registry.", fg=typer.colors.RED)
            
    except FileNotFoundError:
        typer.secho(f"❌ Blueprint file '{blueprint_file}' missing. Initialize first using 'build-profile'.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()
