import numpy as np
import collections
import copy


class GomokuBoard:
    def __init__(self, height=19, width=19):
        self.shape = np.array([height, width])
        self.board_data = np.zeros(self.shape)
        self.deque = collections.deque(maxlen=400)

    def show(self):
        print("Player1: X\tPlayer2: O")
        print("{0: >4}".format(""), end="")
        for i in range(self.shape[1]):
            print("{0: >3}".format(i+1), end="")
        print("")
        for i in range(self.shape[0]):
            print("{0: >4}".format(i+1), end="")
            for j in range(self.shape[1]):
                if self.board_data[i, j] == 0:
                    show_label = "-"
                if self.board_data[i, j] == 1:
                    show_label = "X"
                if self.board_data[i, j] == 2:
                    show_label = "O"
                print("{0: >3}".format(show_label), end="")
            print("")

    def set_value(self, h_position, v_position, player_value):
        if h_position > self.shape[0]:
            return False
        if v_position > self.shape[1]:
            return False
        if self.board_data[h_position, v_position] != 0:
            return False
        if player_value != 1 and player_value != 2:
            return False
        self.board_data[h_position, v_position] = player_value
        self.deque.append(copy.copy(self.board_data))
        return True

    def reset(self):
        self.board_data = np.zeros(self.shape)
        self.deque.clear()
        for _ in range(10):
            self.deque.append(copy(self.board_data))


if __name__ == "__main__":
    board = GomokuBoard()
    board.set_value(5, 5, 1)
    board.set_value(6, 6, 2)
    board.show()
