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
