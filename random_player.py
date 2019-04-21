import random


class GomokuPlayer:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_action(self, board):
        if board.last_step[0] == -1:
            pass
        elif board.board_data[board.last_step[0], board.last_step[1]] == self.player_id:
            return

        return random.choice(board.valid_position)