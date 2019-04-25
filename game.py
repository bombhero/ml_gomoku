from board import GomokuBoard
from mcts_player import GomokuPlayer
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
        for i in range(self.gomoku_board.shape[0] - self.row_in_line):
            for j in range(self.gomoku_board.shape[1] - self.row_in_line):
                hold_value = self.gomoku_board.board_data[i, j]
                if hold_value == 0:
                    continue
                might_winner = [True, True, True]
                for row in range(1, self.row_in_line):
                    if self.gomoku_board.board_data[i + row, j] != hold_value:
                        might_winner[0] = False
                    if self.gomoku_board.board_data[i + row, j + row] != hold_value:
                        might_winner[1] = False
                    if self.gomoku_board.board_data[i, j + row] != hold_value:
                        might_winner[2] = False
                    if might_winner == [False, False, False]:
                        break
                for row in range(3):
                    if might_winner[row]:
                        winner = hold_value
                if winner != 0:
                    game_end = True
                    break
            if game_end:
                break
        return game_end, winner


def run():
    game = GomokuGame(height=6,width=6, row_in_line=4)
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

                time.sleep(10)
                break


if __name__ == "__main__":
    run()
