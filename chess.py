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
