import numpy as np
import collections
import copy
import matplotlib.pyplot as plt


class GomokuBoard:
    def __init__(self, height=19, width=19):
        self.shape = np.array([height, width])
        self.board_data = np.zeros(self.shape)
        self.deque = collections.deque(maxlen=400)
        self.last_step = [-1, -1]
        self.base_show = False
        self.valid_position = list(range(height * width))

    def show(self, show_pic=False):
        print("Player1: X\tPlayer2: O")
        print("{0: >4}".format(""), end="")
        for i in range(self.shape[1]):
            print("{0: <3}".format(i+1), end="")
        print("")
        for i in range(self.shape[0]):
            print("{0: <4}".format(i+1), end="")
            for j in range(self.shape[1]):
                if self.board_data[i, j] == 0:
                    show_label = "-"
                if self.board_data[i, j] == 1:
                    show_label = "X"
                if self.board_data[i, j] == 2:
                    show_label = "O"
                if i == self.last_step[0] and j == self.last_step[1]:
                    show_label = show_label+")"
                print("{0: <3}".format(show_label), end="")
            print("")
        if show_pic:
            self.show_pic()

    def show_pic(self):
        if not self.base_show:
            for i in range(self.shape[0]):
                plt.plot([0, self.shape[1] - 1], [i, i], "b-")
            for j in range(self.shape[1]):
                plt.plot([j, j], [0, self.shape[0] - 1], "b-")
            self.base_show = True
        if self.last_step != [-1, -1]:
            if self.board_data[self.last_step[0], self.last_step[1]] == 1:
                plt.plot([self.last_step[1]], [self.last_step[0]], "ko")
            if self.board_data[self.last_step[0], self.last_step[1]] == 2:
                plt.plot([self.last_step[1]], [self.last_step[0]], "yo")
        plt.ion()
        plt.show()
        plt.pause(0.01)

    def set_value(self, h_position, v_position, player_value):
        position = h_position * self.shape[1] + v_position
        if position not in self.valid_position:
            return False
        if player_value != 1 and player_value != 2:
            return False
        self.board_data[h_position, v_position] = player_value
        self.last_step = [h_position, v_position]
        self.valid_position.remove(position)
        self.deque.append(copy.copy(self.board_data))
        return True

    def reset(self, ):
        self.board_data = np.zeros(self.shape)
        self.deque.clear()
        for _ in range(10):
            self.deque.append(copy(self.board_data))


if __name__ == "__main__":
    board = GomokuBoard()
    board.set_value(5, 5, 1)
    board.set_value(6, 6, 2)
    board.show()
