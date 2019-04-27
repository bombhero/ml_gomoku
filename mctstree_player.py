import random
import copy
import numpy as np


class TreeNode:
    def __init__(self, parent, position, game):
        self._parent = parent
        self._position = position
        self._n_visit = 0
        self._n_reward = 0
        self._game_copy = game
        self._child = {}

    def is_leaf(self):
        if len(self._child) == 0:
            return True
        else:
            return False


class MCTS:
    def __init__(self):
        self._root = TreeNode(None, -1)

    def get_move(self, game):
        return 0


class GomokuPlayer:
    def __init__(self, player_id):
        self.mcts = MCTS()
        self.player_id = player_id

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1

        return self.mcts.get_move(game)
