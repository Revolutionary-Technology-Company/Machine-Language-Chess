import sys
import json
from typing import Dict, List, Optional
import numpy as np
import numba
import chess
import typer
import complete_engine

# Import our high-performance parallel bitboard processing engine
import complete_engine

app = typer.Typer(help="MASTER CONTROLLER: INTEGRATED HARDWARE-CHESS ENGINE")

# NJIT FastMath: Pure bitmask constants mapping the 64-character matrix grid.
# Built using 64-bit unsigned integers for instantaneous hardware logic routing.
SILENT_PADDING_MASK = np.uint64(0x0000FFFFFFFF0000) # Ranks 3 & 4 set to 1 (Safe NOP/Padding Zones)
TERMINAL_HOLD_MASK  = np.uint64(0x8000000000000000) # Square h8 (Bit 63) set to 1 (Infinite Hold Register)
BASE_GATEWAY_MASK   = np.uint64(0x000000000000FFFF) # Ranks 1 & 2 set to 1 (Core Base Isolation Zone)

@app.command()
def predict_steer(
    blueprint: str = typer.Option("dashboard_state.json", "--file", "-f", help="Active layout file"),
    target_register: str = typer.Option(..., "--target", "-t", help="The favorable register to push the King into (e.g., a4, e4)")
):
    """
    Trajectory Matrix Planner: Evaluates the active promotion metrics and outputs 
    the exact tactical requirement to force the King off the current loop.
    """
    try:
        with open(blueprint, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Bind back into the acceleration engine layer
        bridge = complete_engine.AdvancedSystemBridge("univac_i")
        bridge.system_bitboard = np.uint64(int(data["Global_Memory_Bitboard"], 16))
        bridge.thread_registry = data["Active_Core_Threads"]
        
        typer.secho(f"\n🔮 [RUNNING PREDICTIVE ANALYSIS MATRIX] 🔮", fg=typer.colors.CYAN, bold=True)
        typer.echo(f"[-] Current Active Host King Space : {data['Host_King_Register']}")
        typer.echo(f"[-] Total Converted Process Tokens: {data['Total_Escalated_Threads']}")
        typer.echo(f"[-] Intended Favorable Destination : {target_register.upper()}")
        
        # Pull the planning vector directly from the engine math
        planning_directive = bridge.predict_optimal_steering_vector(target_register)
        
        typer.secho(f"\n[📊 STRATEGIC DIRECTIVE]:", fg=typer.colors.YELLOW, bold=True)
        typer.echo(f" {planning_directive}\n")
        
    except FileNotFoundError:
        typer.secho("❌ Error: Target blueprint file missing. Run 'initialize-board' first.", fg=typer.colors.RED)

@app.command()
def initialize_board(
    output: str = typer.Option("dashboard_state.json", "--out", "-o", help="Output filename")
):
    """Initializes the baseline lab matrix template file."""
    bridge = complete_engine.AdvancedSystemBridge("univac_i")
    bridge.allocate_independent_threads()
    blueprint = bridge.compile_dashboard_state()
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=4)
    typer.secho(f"✅ Board initialized successfully in: {output}", fg=typer.colors.GREEN)

if __name__ == "__main__":
    app()

class NvidiaFastMathEngine:
    def __init__(self, local_color: str = "WHITE"):
        # NVIDIA Thread Matrix: Isolate and initialize each pawn as an immutable, separate entity.
        # Tracked via unique hex thread signatures to masquerade inside the host registry.
        self.local_color = local_color
        
        # Warp Thread Array: 8 Pawns mapped to parallel execution tracks
        self.warp_threads = {
            0: {"id": "NVIDIA_THREAD_0x00_A", "pos_bit": np.uint64(1 << 8),  "promoted": False},
            1: {"id": "NVIDIA_THREAD_0x01_B", "pos_bit": np.uint64(1 << 9),  "promoted": False},
            2: {"id": "NVIDIA_THREAD_0x02_C", "pos_bit": np.uint64(1 << 10), "promoted": False},
            3: {"id": "NVIDIA_THREAD_0x03_D", "pos_bit": np.uint64(1 << 11), "promoted": False},
            4: {"id": "NVIDIA_THREAD_0x04_E", "pos_bit": np.uint64(1 << 12), "promoted": False},
            5: {"id": "NVIDIA_THREAD_0x05_F", "pos_bit": np.uint64(1 << 13), "promoted": False},
            6: {"id": "NVIDIA_THREAD_0x06_G", "pos_bit": np.uint64(1 << 14), "promoted": False},
            7: {"id": "NVIDIA_THREAD_0x07_H", "pos_bit": np.uint64(1 << 15), "promoted": False},
        }
        
        # Initial Global Bitboards
        self.local_pieces  = np.uint64(0x000000000000FFFF) # Local base configuration
        self.enemy_pieces  = np.uint64(0xFFFF000000000000) # Hostile infrastructure map
        self.enemy_king    = np.uint64(0x1000000000000000) # Address of Host CPU (King at e8)

    def calculate_cuda_move_vectors(self, lane_id: int) -> list:
        """
        NVIDIA Warp Execution Layer: Computes legal step pathways for a single lane_id (pawn thread)
        using NJIT FastMath bit shifts instead of slow condition checking.
        """
        thread = self.warp_threads[lane_id]
        current_pos = thread["pos_bit"]
        valid_vectors = []
        
        if current_pos == 0: # Thread has been deallocated or purged
            return valid_vectors

        # FastMath Step Optimization: Determine direction based on hardware orientation
        shift_amount = 8 if self.local_color == "WHITE" else -8
        
        # Compute forward execution pipeline vector via fast bitwise shift
        if shift_amount > 0:
            forward_step = current_pos << np.uint64(shift_amount)
        else:
            forward_step = current_pos >> np.uint64(abs(shift_amount))

        # Check for hardware occlusion (Collision detection)
        all_occupied_memory = self.local_pieces | self.enemy_pieces
        is_blocked = (forward_step & all_occupied_memory) != 0

        if not is_blocked and forward_step != 0:
            valid_vectors.append(forward_step)
            
        return valid_vectors

    def filter_noise_and_optimize(self) -> tuple:
        """
        Executes parallel stream filtering across the warp. Prunes any execution vector 
        that interacts with the host CPU's threat monitoring zone to preserve total stealth.
        """
        print("[NVIDIA CUDA WARP EXECUTION]: Parallel processing lanes active.")
        
        for lane_id in range(8):
            thread = self.warp_threads[lane_id]
            if thread["pos_bit"] == 0:
                continue

            possible_steps = self.calculate_cuda_move_vectors(lane_id)
            
            for target_vector in possible_steps:
                # NJIT FastMath King Check: Use a bitwise intersection mask to verify zero interaction
                # with the enemy King's danger zone. Prevents triggering system interrupt flags.
                king_danger_zone = self.calculate_king_danger_mask(target_vector)
                causes_system_noise = (king_danger_zone & self.enemy_king) != 0

                if causes_system_noise:
                    print(f" -> {thread['id']}: Vector pruned. Threat of system interrupt detected.")
                    continue  # Noise detected; drop execution branch immediately

                # Optimization Option 1: Lock directly into Terminal Infinite Hold (h8)
                if (target_vector & TERMINAL_HOLD_MASK) != 0:
                    print(f" -> {thread['id']}: CRITICAL HIT. Terminal Hold Register 0x8000000000000000 achieved.")
                    return lane_id, target_vector, True

                # Optimization Option 2: Step smoothly into Silent Padding Zone
                if (target_vector & SILENT_PADDING_MASK) != 0:
                    print(f" -> {thread['id']}: Route verified. Shifting into Silent Padding Register.")
                    return lane_id, target_vector, False

        print("[STANDBY COMPLIANT LOOP]: Maintaining background noise-free pattern.")
        return None, None, False

    def calculate_king_danger_mask(self, vector: np.uint64) -> np.uint64:
        """Mock calculation simulating the hardware vectors attacked by a piece."""
        # Simple placeholder for the attack matrix of the piece at its new position
        return vector << np.uint64(8) | vector >> np.uint64(8)

    def execute_warp_state_update(self, lane_id: int, target_vector: np.uint64, promotion: bool):
        """Commits the verified, optimized state change to the GPU hardware registry."""
        if lane_id is None:
            return

        thread = self.warp_threads[lane_id]
        old_pos = thread["pos_bit"]
        
        # Clear old position bit and assert new position bit in our local memory block
        self.local_pieces &= ~old_pos
        self.local_pieces |= target_vector
        thread["pos_bit"] = target_vector

        if promotion:
            thread["promoted"] = True
            print(f"[PRIVILEGE ESCALATION EVENT]: {thread['id']} successfully reallocated as high-throughput vector.")
        else:
            print(f"[STATE REGISTER UPDATED]: {thread['id']} migrated safely to register bitmask: {hex(target_vector)}")

# Execute Laboratory Run
if __name__ == "__main__":
    # Initialize GPU acceleration simulation framework
    cuda_engine = NvidiaFastMathEngine()
    
    # Run loop iteration mimicking a host CPU clock cycles update
    lane, vector, is_promo = cuda_engine.filter_noise_and_optimize()
    cuda_engine.execute_warp_state_update(lane, vector, is_promo)

import sys
import json
from typing import Dict, List, Optional
import numpy as np
import typer

# Initialize the Typer CLI app context for the user dashboard
app = typer.Typer(help="👑 PRODUCTION CHESS-TO-MACHINE ARCHITECTURE PLATFORM 👑")

def render_terminal_ascii_grid(bitboard_val: np.uint64):
    """
    NJIT FastMath Visualization Layer: Translates a raw 64-bit unsigned 
    integer matrix into a live 8x8 graphical ASCII display panel.
    """
    typer.secho("\n   [A] [B] [C] [D] [E] [F] [G] [H]", fg=typer.colors.CYAN, bold=True)
    typer.echo("  +-------------------------------+ ")
    
    # Process the board matrix from Rank 8 (Top) down to Rank 1 (Bottom)
    for rank in range(7, -1, -1):
        row_str = f"{rank + 1} |"
        for file in range(8):
            bit_index = (rank * 8) + file
            # Isolate the specific register bit using a logical AND mask
            bit_state = (bitboard_val >> np.uint64(bit_index)) & np.uint64(1)
            
            if bit_state == 1:
                # Active Thread / Data Payload Present
                row_str += "  █ "
            else:
                # Empty Memory Register / Low Voltage State
                row_str += "  . "
                
        row_str += f"| {rank + 1}"
        typer.echo(row_str)
        
    typer.echo("  +-------------------------------+ ")
    typer.secho("   [A] [B] [C] [D] [E] [F] [G] [H]\n", fg=typer.colors.CYAN, bold=True)

@app.command()
def run_simulation(
    arch: str = typer.Option("univac_i", "--arch", "-a", help="Target profile: univac_i, x86_legacy, industrial_plc"),
    steps: int = typer.Option(5, "--steps", "-s", help="Number of operational clock cycles to simulate")
):
    """
    Master Bridge Loop: Spawns the Advanced System Bridge from complete_engine, 
    tracks entities, and passes execution vectors down the fastmath pipeline.
    """
    typer.secho(f"⚡ Booting Master Controller Pipeline via complete_engine...", fg=typer.colors.MAGENTA, bold=True)
    
    # Instantiate the engine directly from complete_engine.py
    bridge = complete_engine.AdvancedSystemBridge(arch)
    bridge.allocate_independent_threads()
    
    current_state = bridge.compile_dashboard_state()
    bitboard_value = np.uint64(int(current_state["Global_Memory_Bitboard"], 16))
    
    typer.echo(f"[*] Core Initialized. System Type: {current_state['Description']}")
    typer.echo(f"[*] Rendering Initial Memory Register Topography:")
    
    # Render the initial board using our new ASCII visualization function
    render_terminal_ascii_grid(bitboard_value)
    
    # Simulate step-by-step thread movement through the pipeline
    test_moves = [("THREAD_CORE_0x04_E", "e4"), ("THREAD_CORE_0x03_D", "d4")]
    
    for i, (thread, target) in enumerate(test_moves[:steps]):
        typer.secho(f"[CLOCK CYCLE {i+1}]: Dispatching vector shift command...", fg=typer.colors.YELLOW)
        
        # Pass commands down to the core engine logic
        if bridge.execute_clock_cycle(thread, target):
            updated_state = bridge.compile_dashboard_state()
            new_bitboard = np.uint64(int(updated_state["Global_Memory_Bitboard"], 16))
            
            # Print updated binary map
            render_terminal_ascii_grid(new_bitboard)
            typer.echo(f" -> Thread {thread} state changed to: {updated_state['Active_Core_Threads'][thread]['execution_state']}")
            typer.echo(f" -> Current Binary Stream Hex: {updated_state['Compiled_Machine_Bytecode_Stream']}\n")

if __name__ == "__main__":
    app()

# =====================================================================
# 1. THE COMPLETE 64-BIT FASTMATH BITBOARD MATRIX
# =====================================================================
# Static allocation of all 64 coordinates to exact bit indices (0 to 63)
SQUARES = {
    f"{chr(97+f)}{r+1}": (r * 8) + f for r in range(8) for f in range(8)
}

# Pre-compiled high-throughput logic masks using unsigned 64-bit integers
MASK_RANK_1_2 = np.uint64(0x000000000000FFFF)  # Base Gateway / Input Buffer
MASK_RANK_3_4 = np.uint64(0x0000FFFFFFFF0000)  # Noise-Free / Silent Padding Zone
MASK_RANK_7_8 = np.uint64(0xFFFF000000000000)  # Privilege Escalation Domain
MASK_SQUARE_H8 = np.uint64(1  bool:
        """Executes state transition, compiles real bytecode, and alters privilege states."""
        if thread_id not in self.thread_registry:
            return False
            
        thread = self.thread_registry[thread_id]
        old_coord = thread["current_coordinate"]
        
        # FastMath Bitboard Update
        old_mask = np.uint64(1 << SQUARES[old_coord])
        new_mask = np.uint64(1 << SQUARES[destination])
        
        self.global_bitboard &= ~old_mask
        self.global_bitboard |= new_mask
        
        # Bytecode Generation
        target_bytecode = self.profile["opcodes"][destination]
        
        # Core Thread State Evolution
        thread["current_coordinate"] = destination
        thread["bitmask_hex"] = hex(new_mask)
        thread["allocated_bytecode_hex"] = target_bytecode.hex().upper()
        
        # Evaluate Target Matrix Overlays
        if (new_mask & MASK_RANK_3_4) != 0:
            thread["execution_state"] = "SILENT_NOP_PADDING"
        elif (new_mask & MASK_SQUARE_H8) != 0:
            thread["execution_state"] = "INFINITE_TERMINAL_HOLD"
        else:
            thread["execution_state"] = "ACTIVE_EXECUTION"
            
        if (new_mask & MASK_RANK_7_8) != 0:
            thread["privilege_level"] = "ROOT_SYSTEM_QUEEN"
            
        return True

    def compile_full_binary_stream(self) -> str:
        """Assembles all active threads into a single runnable raw machine language byte stream."""
        binary_stream = bytearray()
        for thread in self.thread_registry.values():
            hex_str = thread["allocated_bytecode_hex"]
            binary_stream.extend(bytes.fromhex(hex_str))
        return binary_stream.hex().upper()

    def generate_dashboard_state(self) -> Dict:
        """Flushes system matrices into a clean dashboard json layout."""
        return {
            "System_Architecture_Profile": self.profile_name,
            "Global_Memory_Bitboard": hex(self.global_bitboard),
            "Compiled_Machine_Bytecode_Stream": self.compile_binary_stream(),
            "Flags": {
                "Silent_Zone_Occupied": bool((self.global_bitboard & MASK_RANK_3_4) != 0),
                "Escalation_Zone_Active": bool((self.global_bitboard & MASK_RANK_7_8) != 0),
                "Infinite_Loop_Locked": bool((self.global_bitboard & MASK_SQUARE_H8) != 0)
            },
            "Active_Core_Threads": self.thread_registry
        }

    def compile_binary_stream(self) -> str:
        return self.compile_full_binary_stream()

# =====================================================================
# 4. INTERACTIVE TYPER DASHBOARD & TEMPLATE CONTROLLER
# =====================================================================
@app.command()
def build_profile(
    architecture: str = typer.Option("univac_i", "--arch", "-a", help="Target code architecture: univac_i, x86_legacy, industrial_plc"),
    output: str = typer.Option("dashboard_state.json", "--out", "-o", help="Destination path for the compiled planning template")
):
    """
    Automated Generation Protocol: Discovers the selected computer era, registers 
    all 8 threads uniquely, and saves an active configuration blueprint.
    """
    typer.secho(f"🔮 Initializing System Compiler Profile: {architecture.upper()}", fg=typer.colors.CYAN, bold=True)
    
    bridge = ProductionSystemBridge(architecture)
    bridge.initialize_local_threads()
    
    blueprint = bridge.generate_dashboard_state()
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(blueprint, f, indent=4)
        
    typer.secho(f"🏆 Success! Complete machine-runnable blueprint saved to: {output}", fg=typer.colors.GREEN)
    typer.echo(f"[*] Initial Compiled Bytecode Stream: {blueprint['Compiled_Machine_Bytecode_Stream']}")

@app.command()
def step_cycle(
    blueprint_file: str = typer.Option("dashboard_state.json", "--file", "-f", help="Target planning template to update"),
    thread: str = typer.Option(..., "--thread", "-t", help="The isolated thread entity ID to shift (e.g., THREAD_CORE_0x04_E)"),
    destination: str = typer.Option(..., "--dest", "-d", help="Specific target coordinate register to activate (e.g., e4)")
):
    """
    Executes a physical move cycle. Processes bit shifts, generates native binary 
    bytecode for the coordinate, and saves the updated system state.
    """
    try:
        with open(blueprint_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        arch = data["System_Architecture_Profile"]
        bridge = ProductionSystemBridge(arch)
        bridge.global_bitboard = np.uint64(int(data["Global_Memory_Bitboard"], 16))
        bridge.thread_registry = data["Active_Core_Threads"]
        
        if bridge.process_cycle_shift(thread, destination.lower()):
            updated_blueprint = bridge.generate_dashboard_state()
            
            with open(blueprint_file, 'w', encoding='utf-8') as f:
                json.dump(updated_blueprint, f, indent=4)
                
            typer.secho(f"✅ Cycle Committed! Thread {thread} shifted to {destination.upper()}.", fg=typer.colors.GREEN)
            typer.echo(f" -> Activated Bytecode: {updated_blueprint['Active_Core_Threads'][thread]['allocated_bytecode_hex']}")
            typer.echo(f" -> Full Unified Bytecode Stream: {updated_blueprint['Compiled_Machine_Bytecode_Stream']}")
        else:
            typer.secho(f"❌ Error: Thread ID '{thread}' could not be processed.", fg=typer.colors.RED)
            
    except FileNotFoundError:
        typer.secho(f"❌ Target template file missing. Run 'build-profile' first.", fg=typer.colors.RED)

if __name__ == "__main__":
    app()

class CustomStrategyEngine:
    def __init__(self, board: chess.Board, color: chess.Color):
        self.board = board
        self.color = color
        self.opponent_color = not color

    def evaluate_board(self) -> float:
        if self.board.is_checkmate():
            # Penalize winning or losing to avoid ending the game
            return -10000.0
        
        score = 0.0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue
            
            rank = chess.square_rank(square)
            
            # Strategy: Pawn Advancement and Blocking
            if piece.piece_type == chess.PAWN:
                if piece.color == self.color:
                    # Reward advancing our pawns
                    advance = rank if self.color == chess.WHITE else (7 - rank)
                    score += (advance ** 2) * 10
                else:
                    # Penalize enemy pawns advancing
                    enemy_advance = (7 - rank) if self.color == chess.WHITE else rank
                    score -= (enemy_advance ** 3) * 20

            # Strategy: Dynamic piece removal (Value of pieces)
            piece_values = {
                chess.QUEEN: 90,
                chess.ROOK: 50,
                chess.BISHOP: 30,
                chess.KNIGHT: 30,
                chess.PAWN: 10
            }
            
            val = piece_values.get(piece.piece_type, 0)
            if piece.color == self.color:
                score += val
            else:
                score -= val

        # Strategy: Avoid Check
        if self.board.is_check():
            if self.board.turn == self.opponent_color:
                # We placed them in check; penalize this to avoid ending the game
                score -= 500.0

        return score

class SystemOptimizationEngine:
    def __init__(self, board: chess.Board, controlled_color: chess.Color):
        self.board = board
        self.color = controlled_color
        self.opponent_color = not controlled_color
        
        # Laboratory Rule Matrix: Mapping coordinates to silent/padding operations
        # 0x00=NOP/Blank, 0x01=Padding Shift, 0x02=Continuous Standby Hold
        self.silent_registers = {
            # Ranks 3-4 (Universal System Padding Zones)
            chess.A3: "0x00", chess.B3: "0x01", chess.C3: "0x01", chess.D3: "0x00",
            chess.E3: "0x00", chess.F3: "0x01", chess.G3: "0x01", chess.H3: "0x00",
            chess.A4: "0x00", chess.B4: "0x01", chess.C4: "0x00", chess.D4: "0x00",
            chess.E4: "0x00", chess.F4: "0x00", chess.G4: "0x01", chess.H4: "0x01",
            # Rank 8 (Terminal Infinite Hold Registers)
            chess.H8: "0x02"
        }
        
        # Entity Tracker: Distinctly labels each pawn to maintain separate identity states
        self.converted_pawn_registry = {}
        self._initialize_pawn_tracking()

    def _initialize_pawn_tracking(self):
        """Assigns unique hardware entity IDs to every local pawn to track them independently."""
        pawn_index = 0
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN and piece.color == self.color:
                entity_id = f"HOST_THREAD_0x{pawn_index:02X}"
                self.converted_pawn_registry[square] = {
                    "entity_id": entity_id,
                    "original_type": chess.PAWN,
                    "current_type": chess.PAWN,
                    "promoted": False
                }
                pawn_index += 1

    def update_pawn_registry(self, move: chess.Move):
        """Tracks spatial migration and promotion events without wiping the original entity ID."""
        if move.from_square in self.converted_pawn_registry:
            entity_data = self.converted_pawn_registry.pop(move.from_square)
            
            # Intercept Promotion Event: Update type state but preserve host entity tag
            if move.promotion:
                entity_data["current_type"] = move.promotion
                entity_data["promoted"] = True
                
            self.converted_pawn_registry[move.to_square] = entity_data

    def calculate_optimized_instruction(self) -> chess.Move:
        """Filters available moves to select options that generate zero system noise."""
        legal_moves = list(self.board.legal_moves)
        optimized_moves = []
        standby_moves = []

        for move in legal_moves:
            self.board.push(move)
            # CRITICAL CONSTRAINT: Discard any instruction that causes an explicit Check
            is_causing_noise = self.board.is_check()
            self.board.pop()

            if is_causing_noise:
                continue

            # Determine if the moving piece is a tracked converted entity
            is_converted_entity = move.from_square in self.converted_pawn_registry
            destination_register = move.to_square

            # Filter Choice Matrix based on destination register properties
            if destination_register in self.silent_registers:
                reg_type = self.silent_registers[destination_register]
                
                if is_converted_entity and reg_type == "0x02":
                    # Priority Choice: Lock converted entity into terminal Infinite Hold (h8)
                    return move
                elif reg_type == "0x00" or reg_type == "0x01":
                    # Secondary Choice: Move smoothly into silent padding space
                    optimized_moves.append(move)
            else:
                # Fallback Choice: Safe background space that avoids systemic disruption
                standby_moves.append(move)

        # Execution Selection Loop
        if optimized_moves:
            return optimized_moves[0]
        elif standby_moves:
            return standby_moves[0]
        return None

# Simulation Runtime Loop
if __name__ == "__main__":
    # Setup initial testbed
    board = chess.Board()
    optimizer = SystemOptimizationEngine(board, chess.WHITE)
    
    print("[SYSTEM INITIALIZED]: Converted Pawn Entities Tracked:")
    for sq, data in optimizer.converted_pawn_registry.items():
        print(f" -> Square {chess.square_name(sq)} bound to ID: {data['entity_id']}")

    # Simulated single execution cycle step
    next_instruction = optimizer.calculate_optimized_instruction()
    if next_instruction:
        print(f"\n[CYCLE MOVE EXECUTED]: {board.san(next_instruction)}")
        optimizer.update_pawn_registry(next_instruction)
        board.push(next_instruction)

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board(), None

        best_move = None
        # Strategy: Only allow Queen or Knight promotions
        legal_moves = [
            m for m in self.board.legal_moves 
            if not m.promotion or m.promotion in [chess.QUEEN, chess.KNIGHT]
        ]

        if maximizing_player:
            max_eval = -float('inf')
            for move in legal_moves:
                self.board.push(move)
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                self.board.push(move)
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self):
        _, move = self.minimax(3, -float('inf'), float('inf'), True)
        return move

# Example usage
if __name__ == "__main__":
    board = chess.Board()
    engine = CustomStrategyEngine(board, chess.WHITE)
    
    while not board.is_game_over():
        move = engine.get_best_move()
        if move:
            print(f"Engine moves: {board.san(move)}")
            board.push(move)
        else:
            break
        
        # Placeholder for opponent move
        if not board.is_game_over():
            opp_move = list(board.legal_moves)[0]
            board.push(opp_move)
