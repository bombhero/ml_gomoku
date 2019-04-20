from board import GomokuBoard
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

    def whose_term(self):
        if self.term_owner == 0:
            self.term_owner = random.randint(1, 2)
        return self.term_owner

    def has_winner(self):
        winner = 0
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
                    return winner
        return winner


if __name__ == "__main__":
    game = GomokuGame()
    for e in range(300):
        player = game.whose_term()
        position = random.choice(game.gomoku_board.valid_position)
        h = int(position / game.shape[1])
        v = position - h * game.shape[1]
        ret = game.step(player, h, v)
        if ret:
            game.gomoku_board.show(show_pic=True)
            # time.sleep(10)
        else:
            print("Position {},{} is not valid".format(h, v))
            break
        winner = game.has_winner()
        if winner != 0:
            print("Player{} Win in {}!!!".format(winner, e))
            print("h={}, v={}.".format(h+1, v+1))
            print(len(game.gomoku_board.deque))
            last_step = game.gomoku_board.deque[1]
            break
    time.sleep(30)

