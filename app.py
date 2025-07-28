from flask import Flask, request, jsonify
from match import Match
from board import Board
from pieces import Man, King
from player import Player
import uuid 

app = Flask(__name__)
games = {} # Your in-memory store for games

@app.route('/api/games', methods=['POST'])
def create_game():
    game_id = str(uuid.uuid4())
    new_match = Match() # Assuming Match is imported and available
    games[game_id] = new_match
    return jsonify({"game_id": game_id, "message": "Game created successfully!"}), 201


@app.route('/api/games/<game_id>/board', methods=['GET'])
def get_board_state(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    board_state = []
    for r in range(8):
        row_data = []
        for c in range(8):
            piece = game.board.grid[r][c]
            if piece:
                row_data.append({
                    "type": "king" if piece.is_king else "man",
                    "color": piece.color,
                    "position": piece.position
                })
            else:
                row_data.append(None)
        board_state.append(row_data)

    return jsonify({
        "game_id": game_id,
        "current_player_color": game.players[game.current_player_index].color,
        "board": board_state
    })

@app.route('/api/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    current_player = game.players[game.current_player_index]
    if not current_player.has_moves(game.board):
        return jsonify({"message": f"{current_player.color} cannot move. Game over."}), 200 # Or 400 bad request

    data = request.get_json()
    from_pos = tuple(data.get('from_position'))
    # For simplicity, this example only handles simple moves.
    # Full capture path handling would be more complex and need to mirror match.py logic.
    to_pos = tuple(data.get('to_position'))

    piece = game.board.get_piece_at(from_pos)

    if not piece or piece.color != current_player.color:
        return jsonify({"error": "Invalid piece selected or not your piece"}), 400

    capturing_pieces = current_player.get_pieces_with_captures(game.board)
    if capturing_pieces and piece not in capturing_pieces:
        return jsonify({"error": "You must play a piece that can capture."}), 400

    if game.board.get_all_captures(piece):
        # This part needs significant re-work to handle capture paths via API
        # For a full API, you'd need to accept a 'capture_path' list.
        # This example will not fully implement multi-capture logic via API input.
        return jsonify({"error": "Captures are required. API for multi-capture not yet fully implemented."}), 400

    if to_pos in game.board.get_simple_moves(piece):
        game.board.move_piece(piece, to_pos)
        game.switch_turn()
        return jsonify({"message": "Move successful", "new_board_state": f"/api/games/{game_id}/board"}), 200
    else:
        return jsonify({"error": "Invalid move"}), 400

if __name__ == '__main__':
    app.run(debug=True)