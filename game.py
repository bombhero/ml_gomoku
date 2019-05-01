from board import GomokuBoard
from mctstree_player import GomokuPlayer
import random
import time


class GomokuGame:
    def __init__(self, height=19, width=19, row_in_line=5):
        self.gomoku_board = GomokuBoard(height, width)
        self.shape = self.gomoku_board.shape
        self.row_in_line = row_in_line
        self.term_owner = 0
        self.last_step = [0, 0, 0]

    def step(self, player, h_position, v_position, is_show=False):
        if player != self.term_owner:
            print("Should be player{} term".format(self.term_owner))
            return False
        ret = self.gomoku_board.set_value(h_position, v_position, player)
        if ret:
            self.last_step = [h_position, v_position, player]
        if is_show:
            self.gomoku_board.show()
        if self.term_owner == 1:
            self.term_owner = 2
        else:
            self.term_owner = 1
        return ret

    def do_move(self, position, is_show=False):
        h = int(position / self.shape[1])
        v = position - h * self.shape[1]
        self.step(self.whose_term(), h, v, is_show)

    def whose_term(self):
        if self.term_owner == 0:
            self.term_owner = random.randint(1, 2)
        return self.term_owner

    def game_end(self):
        winner = 0
        game_end = False

        # The board id full
        if len(self.gomoku_board.valid_position) == 0:
            return True, 0

        for i in range(self.gomoku_board.shape[0]):
            for j in range(self.gomoku_board.shape[1]):
                hold_value = self.gomoku_board.board_data[i, j]
                if hold_value == 0:
                    continue
                might_win = [True, True, True]
                for row in range(self.row_in_line):
                    if i + row >= self.gomoku_board.shape[0] or hold_value != self.gomoku_board.board_data[i+row, j]:
                        might_win[0] = False
                        break
                for row in range(self.row_in_line):
                    if j + row >= self.gomoku_board.shape[1] or hold_value != self.gomoku_board.board_data[i, j+row]:
                        might_win[1] = False
                        break
                for row in range(self.row_in_line):
                    if i + row >= self.gomoku_board.shape[0] or j + row >= self.gomoku_board.shape[1] \
                            or hold_value != self.gomoku_board.board_data[i+row, j+row]:
                        might_win[2] = False
                        break
                if might_win != [False, False, False]:
                    game_end = True
                    winner = hold_value

        return game_end, winner


def run():
    game = GomokuGame(height=15, width=15, row_in_line=5)
    player = []
    for player_id in [1, 2]:
        player.append(GomokuPlayer(player_id))
    for r in range(5):
        game.gomoku_board.reset()
        for e in range(300):
            player_id = game.whose_term()
            if player[0].player_id == player_id:
                position = player[0].get_action(game)
            else:
                position = player[1].get_action(game)
            h = int(position / game.shape[1])
            v = position - h * game.shape[1]
            ret = game.step(player_id, h, v)
            if ret:
                game.gomoku_board.show(show_pic=True)
                # time.sleep(10)
            else:
                print("Position {},{} is not valid".format(h, v))
                break
            game_end, winner = game.game_end()
            if game_end:
                if winner != 0:
                    print("Player{} Win in {}!!!".format(winner, e))
                    print("h={}, v={}.".format(h+1, v+1))
                else:
                    print("No winner, board is full!!!")

                time.sleep(30)
                break


if __name__ == "__main__":
    run()
