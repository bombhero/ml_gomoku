import random
import numpy as np
import copy


def rollout_value_fn(game):
    action_n = game.gomoku_board.valid_position
    action_possible = np.random.rand(len(action_n))
    return zip(action_n, action_possible)


def policy_value_fn(game):
    action_n = game.gomoku_board.valid_position
    action_possible = np.ones(len(action_n)) / len(action_n)
    return zip(action_n, action_possible)


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

    def expand(self, action_possible):
        for action, possible in action_possible:
            if action not in self._child:
                self._child[action] = MCTSTreeNode(self, possible)
        pass

    def update(self, reward):
        self._n_visit += 1
        self._Q

    def recursive_update(self, reward):
        if self._parent:
            self._parent.recursive_update(reward)
        self.update(reward)

    def is_leaf(self):
        if len(self._child) == 0:
            return True
        else:
            return False


class MCTSPure:
    def __init__(self, c_put=5, n_playout=100):
        self._root = MCTSTreeNode(None, 1.0)
        self._n_playout = n_playout
        self._c_put = c_put
        self._policy = policy_value_fn
        self._rollout = rollout_value_fn

    def _playout(self, game):
        node = self._root
        while True:
            if node.is_leaf():
                break
            action, node = node.select(self._c_put)
            game.do_move(action)

        game_end, winner = game.game_end()
        if winner == 0:
            action_possible = self._policy(game)
            node.expand(action_possible)
        leaf_value = self._evaluate_rollout(game)
        pass

    def _evaluate_rollout(self, game, limit=400):
        current_player = game.whose_term()
        for i in range(limit):
            game_end, winner = game.game_end()
            if game_end:
                break
            action_possible = self._rollout(game)
            max_action = max(action_possible, key=lambda action:action[1])[0]
            game.do_move(max_action)
        if winner == 0:
            return 0
        else:
            return 1 if winner == current_player else -1

    def get_move(self, game):
        for _ in range(self._n_playout):
            game_copy = copy.deepcopy(game)
            self._playout(game_copy)
        print("Get move done.")


class GomokuPlayer:
    def __init__(self, player_id):
        self.player_id = player_id
        self.mcts = MCTSPure()

    def get_action(self, game):
        if game.whose_term() != self.player_id:
            return -1

        return self.mcts.get_move(game)
