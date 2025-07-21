from match import Match

class Checkers:
    def __init__(self):
        self.match = Match()

    def run(self):
        self.match.start_game()

if __name__ == "__main__":
    game = Checkers()
    game.run()
