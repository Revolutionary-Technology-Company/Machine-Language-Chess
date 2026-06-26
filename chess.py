import chess

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
