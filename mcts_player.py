import random
import numpy as np


class MCTSTreeNode:
    def __init__(self, parent, possible):
        self._parent = parent
        self._possible = possible
        self._n_visit = 0
        self._Q = 0
        self._u = 0
        self._child = {}

    def select(self, c_put):
        return max(self._child.items(), key=lambda action_node: action_node[1].get_value(c_put))

    def get_value(self, c_put):
        self._u = c_put * self._possible * np.sqrt(self._parent._n_visit) / (1 + self._n_visit)
        return self._Q + self._u


class MCTSPure:
    def __init__(self):
        self._root = MCTSTreeNode(None, 1.0)


class GomokuPlayer:
    def __init__(self, player_id):
        self.player_id = player_id
        self.mcts = MCTSPure()

    def get_action(self, board):
        if board.last_step[0] == -1:
            pass
        elif board.board_data[board.last_step[0], board.last_step[1]] == self.player_id:
            return

        return random.choice(board.valid_position)
