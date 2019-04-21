import random


class GomokuPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1

        return random.choice(game.gomoku_board.valid_position)
