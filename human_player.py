class GomokuPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1

        position = input("Input position(h, v): ").split(",")
        h = int(position[0])
        v = int(position[1])
        return game.gomoku_board.shape[1] * (h - 1) + (v - 1)

    def __str__(self):
        return "HumanPlayer"
