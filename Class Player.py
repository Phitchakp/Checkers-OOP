class Player:
    def __init__(self, color):
        self.color = color
        self.pieces = []

    def has_moves(self, board):
        return any(board.get_valid_moves(piece) for piece in self.pieces)

    def get_pieces_with_captures(self, board):
        return [p for p in self.pieces if board.get_all_captures(p)]
    
    