class Match:
    def __init__(self):
        self.board = Board()
        self.players = [Player('dark'), Player('light')]
        self.current_player_index = 0
        self.assign_pieces()

    def assign_pieces(self):
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece_at((r, c))
                if piece:
                    for player in self.players:
                        if player.color == piece.color:
                            player.pieces.append(piece)

    def start_game(self):
        print("Starting Checkers game!")
        self.display_with_highlights()
        while True:
            self.display_with_highlights()
            player = self.players[self.current_player_index]
            print(f"{player.color}'s turn")
            if not player.has_moves(self.board):
                print(f"{player.color} cannot move. Game over.")
                break

            moved = self.make_move(player)
            if moved:
                self.switch_turn()

    def display_with_highlights(self):
        current_player = self.players[self.current_player_index]
        capturing_pieces = current_player.get_pieces_with_captures(self.board)
        self.board.highlight_positions = [p.position for p in capturing_pieces]
        self.board.display()

    def make_move(self, player):
        capturing_pieces = player.get_pieces_with_captures(self.board)
        while True:
            try:
                raw_input = input("Enter piece position to move (row col or type 'GG' to quit): ")
                if raw_input.strip().lower() == 'gg':
                    print("Game ended by user.")
                    exit()
                from_pos = tuple(map(int, raw_input.split()))
                piece = self.board.get_piece_at(from_pos)
                if not piece or piece.color != player.color:
                    print("Invalid piece selected.")
                    continue

                if capturing_pieces and piece not in capturing_pieces:
                    print("You must play a piece that can capture.")
                    continue

                captures = self.board.get_all_captures(piece)
                if captures:
                    print("Multiple captures available:")
                    for i, path in enumerate(captures):
                        print(f"{i + 1}: {path}")
                    choice = int(input("Select capture path number: ")) - 1
                    for next_pos in captures[choice]:
                        mid_row = (piece.position[0] + next_pos[0]) // 2
                        mid_col = (piece.position[1] + next_pos[1]) // 2
                        self.board.grid[mid_row][mid_col] = None
                        self.board.move_piece(piece, next_pos)

                        # After full path, check for additional captures (e.g., after becoming king)
                    while True:
                        new_captures = self.board.get_all_captures(piece)
                        if new_captures:
                            print("Continuing multiple captures with new king...")
                            next_path = new_captures[0]  # default: follow first path
                            for next_pos in next_path:
                                mid_row = (piece.position[0] + next_pos[0]) // 2
                                mid_col = (piece.position[1] + next_pos[1]) // 2
                                self.board.grid[mid_row][mid_col] = None
                                self.board.move_piece(piece, next_pos)
                        else:
                            break
                        # After each move, check for further captures (especially if kinged)
                        new_captures = self.board.get_all_captures(piece)
                        if new_captures:
                            print("Continuing multiple captures with new king...")
                            captures = new_captures
                            choice = 0  # default to first path
                        else:
                            break
                    return True
                else:
                    raw_dest = input("Enter destination position (row col or type 'GG' to quit): ")
                    if raw_dest.strip().lower() == 'gg':
                        print("Game ended by user.")
                        exit()
                    to_pos = tuple(map(int, raw_dest.split()))
                    if to_pos in self.board.get_simple_moves(piece):
                        self.board.move_piece(piece, to_pos)
                        return True
                    else:
                        print("Invalid move. Try again.")
            except Exception as e:
                print("Error in input. Try again.", e)

    def switch_turn(self):
        self.current_player_index = 1 - self.current_player_index


class Checkers:
    def __init__(self):
        self.match = Match()

    def run(self):
        self.match.start_game()


if __name__ == "__main__":
    game = Checkers()
    game.run()
       