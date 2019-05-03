import random
import copy
import numpy as np
import time


def policy_value_fn(game):
    action_probs = np.ones(len(game.gomoku_board.valid_position))/len(game.gomoku_board.valid_position)
    return zip(game.gomoku_board.valid_position, action_probs)


def rollout_policy_fn(game):
    action_probs = np.random.rand(len(game.gomoku_board.valid_position))
    return zip(game.gomoku_board.valid_position, action_probs)


class TreeNode:
    def __init__(self, parent, position, game=None):
        self._parent = parent
        self._position = position
        self._n_visit = 0
        self._n_reward = 0
        self._game_copy = game
        self._children = {}
        self._Q = 0.0
        self._u = 0.0

    def select(self, c_put):
        if len(self._children) == 0:
            return None
        else:
            return max(self._children.items(), key=lambda act_node: act_node[1].get_value(c_put))

    def expand(self, action_priors):
        for action_n, prob in action_priors:
            if action_n not in self._children:
                self._children[action_n] = TreeNode(self, action_n)

    def get_value(self, c_put):
        if (self._n_visit == 0) or (not self._parent):
            return 1.0
        else:
            self._Q = float(self._n_reward) / float(self._n_visit)
            self._u = c_put * np.sqrt(np.log(self._parent._n_visit)/self._n_visit)
            return self._Q + self._u

    def update_value(self, reward):
        self._n_visit += 1
        self._n_reward += reward

    def update_recursive(self, leaf_value):
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update_value(leaf_value)

    def is_leaf(self):
        if len(self._children) == 0:
            return True
        else:
            return False


class MCTS:
    def __init__(self, n_playout=10000, c_put=0.1):
        self._root = TreeNode(None, -1)
        self._n_playout = n_playout
        self._policy = policy_value_fn
        self._rollout = rollout_policy_fn
        self._c_put = c_put

    def _playout(self, game):
        node = self._root
        while True:
            if node.is_leaf():
                break
            action_n, node = node.select(self._c_put)
            game.do_move(action_n)

        game_end, winner = game.game_end()
        if not game_end:
            action_probs = self._policy(game)
            node.expand(action_probs)
        leaf_value = self._evaluate_rollout(game)
        node.update_recursive(-leaf_value)

    def _evaluate_rollout(self, game):
        winner = 0
        current_player = game.whose_term()
        limit = len(game.gomoku_board.valid_position)
        for i in range(limit):
            game_end, winner = game.game_end()
            if game_end:
                break
            action_probs = self._rollout(game)
            max_action = max(action_probs, key=lambda action_node: action_node[1])[0]
            game.do_move(max_action)

        if winner == 0:
            return 0
        else:
            return 1 if winner == current_player else -1

    def get_move(self, game):
        for _ in range(self._n_playout):
            game_copy = copy.deepcopy(game)
            self._playout(game_copy)
        action_n, node = self._root.select(self._c_put)
        return action_n

    def remove_one_child(self, last_move):
        if last_move in self._root._children:
            self._root = self._root._children[last_move]
            self._root._parent = None
        else:
            self._root = TreeNode(None, -1.0)

    def __str__(self):
        return "MCTS"


class GomokuPlayer:
    def __init__(self, player_id):
        self.mcts = MCTS()
        self.player_id = player_id

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1
        if len(game.gomoku_board.valid_position) == 0:
            return -1

        start_ts = time.time()
        move = self.mcts.get_move(game)
        self.mcts.remove_one_child(-1)
        end_ts = time.time()
        print("{} spend {} second.".format(self.__str__(), int(end_ts - start_ts)))
        return move

    def __str__(self):
        return "MctsPlayer"
