import random
import copy
import numpy as np


def rollout_policy_fn(game):
    action_probs = np.random.rand(len(game.gomoku_board.valid_position))
    return zip(game.gomoku_board.valid_position, action_probs)


class TreeNode:
    def __init__(self, parent, position, game):
        self._parent = parent
        self._position = position
        self._n_visit = 0
        self._n_reward = 0
        self._game_copy = game
        self._child = {}

    def select(self):
        if len(self._child):
            return None
        else:
            return max(self._child.items(), key=lambda act_node: act_node[1].get_value())

    def get_value(self):
        if self._n_visit == 0:
            return 1.0
        else:
            return float(self._n_reward) / float(self._n_visit)

    def is_leaf(self):
        if len(self._child) == 0:
            return True
        else:
            return False


class MCTS:
    def __init__(self, n_playout=1000):
        self._root = TreeNode(None, -1)
        self._n_playout = n_playout

    def _playout(self, game):
        node = self._root
        while True:
            if node.is_leaf():
                break
            action_n, node = node.select()
            game.do_move(action_n)

    def get_move(self, game):
        for _ in range(self._n_playout):
            game_copy = copy.deepcopy(game)
            self._playout(game_copy)
        return 0


class GomokuPlayer:
    def __init__(self, player_id):
        self.mcts = MCTS()
        self.player_id = player_id

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1
        if len(game.gomoku_board.valid_position) == 0:
            return -1

        return self.mcts.get_move(game)
