from Agent import Agent
from .MinmaxBoard import MinmaxBoard
from .MinmaxLines import MinmaxLines
from ..BasePolicy import BasePolicy
from ..RandomPolicy.RandomActions import RandomActions
from copy import copy, deepcopy

INFINITE = 1000000
MAX_DEPTH = 3
MAX_MOVE = 15


class Node:
    def __init__(self, board):
        self.board = board
        self.played_piece_pos = None
        self.children = []


class MinmaxPolicy(BasePolicy):
    def __init__(self, agent: Agent):
        super().__init__(agent)
        self.minmax_lines = MinmaxLines(agent.map_size)
        self.action = MinmaxBoard(agent, self.minmax_lines)
        self.random = RandomActions(agent)
        self.agent = agent
        self.executed_cmd = 0

    def evaluation_function(self, lines) -> int:
        """
        Compute the evaluation function of a node
        count the number of piece of the agent and the opponent
        """
        value = 0
        for line in lines:
            value += line.count(1)
            value += line.count(2) * 2
        return value

    def get_children_from_node(self, node, player):
        """ Return all children of a node, which are played move by player one """
        nodes = []
        for move in self.action.get_potential_move(node):
            new_node = Node(deepcopy(node.board))
            self.action.place_piece_on_node(new_node, *move, player)
            new_node.played_piece_pos = move
            nodes.append(new_node)
        return nodes

    def compute_max(self, node, depth, alpha, beta):
        value = -INFINITE
        node.children = self.get_children_from_node(node, self.agent.PlayerState.IA.value)
        for child in node.children:
            value = max(value, self.compute_move(child, depth - 1, True, alpha, beta))
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return value

    def compute_min(self, node, depth, alpha, beta):
        value = INFINITE
        node.children = self.get_children_from_node(node, self.agent.PlayerState.ADVERSARY.value)
        for child in node.children:
            value = min(value, self.compute_move(child, depth - 1, False, alpha, beta))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

    def compute_move(self, node, depth, maximizing_player, alpha, beta) -> int:
        """
        Compute the next move of the agent using the minmax algorithm with alpha-beta pruning
        :param node: current node
        :param depth: depth of the search
        :param maximizing_player: True if the agent is the maximizing player, False otherwise
        :param alpha: alpha value for alpha-beta pruning
        :param beta: beta value for alpha-beta pruning
        :return: the best move
        """
        lines = self.minmax_lines.get_lines_from_node(node, node.played_piece_pos)
        if self.action.check_threat(lines):
            return INFINITE
        if depth == 0:
            return self.evaluation_function(lines)
        if maximizing_player:
            return self.compute_max(node, depth, alpha, beta)
        else:
            return self.compute_min(node, depth, alpha, beta)

    def run_policy(self):
        """ Run the policy """
        root = Node(self.agent.board)
        nodes = self.get_children_from_node(root, self.agent.PlayerState.IA.value)
        if not nodes:
            return self.random.random_move()
        nodes_reward = []
        for move in nodes:
            nodes_reward.append(self.compute_move(move, 1, False, -INFINITE, INFINITE))
        next_move = nodes[nodes_reward.index(max(nodes_reward))]
        self.agent.place_piece(next_move.played_piece_pos, self.agent.PlayerState.IA.value)
        return next_move.played_piece_pos

