import random

from .MinmaxLines import MinmaxLines

THREAT = [[2, 1, 1, 1, 1, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 1, 0], [2, 0, 1, 1, 1, 0, 0],
          [1, 2, 2, 2, 2, 0], [0, 2, 2, 2, 0], [0, 2, 2, 2, 2, 0], [0, 2, 0, 2, 2, 0], [1, 0, 2, 2, 2, 0, 0]]


class MinmaxBoard:
    # Ideas of actions : Attack, Block

    def __init__(self, agent, minmax_lines: MinmaxLines):
        self.agent = agent
        self.enemy_coord = []
        self.possibilities = []
        self.minmax_lines = minmax_lines

    @staticmethod
    def place_piece_on_node(node, x, y, player):
        node.board[y][x] = player

    @staticmethod
    def check_line_threat(line):
        """ Check if a line has a threat """
        for threat in THREAT:
            if threat in line or threat[::-1] in line:
                return True
        return False

    def check_threat(self, lines):
        """ Check if a move has a threat """
        for line in lines:
            if self.check_line_threat(line):
                return True
        return False

    def check_double_threat(self, lines):
        """ Check if a move has a double threat """
        total = 0
        for line in lines:
            if self.check_line_threat(line):
                total += 1
        return total >= 2

    def is_move_worth(self, lines):
        """
        #TODO This can be upgraded
        Check if a move is worth it
        """
        value = 0
        for line in lines:
            value += line.count(self.agent.PlayerState.IA.value)
            value += line.count(self.agent.PlayerState.ADVERSARY.value) * 2
        if value >= 5:
            return True
        return False

    def get_potential_move(self, node) -> [(int, int)]:
        self.possibilities = []
        for i in range(0, self.agent.map_size):
            for j in range(0, self.agent.map_size):
                if self.agent.is_pos_free((i, j)):
                    lines = self.minmax_lines.get_lines_from_node(node, (i, j))
                    if self.check_threat(lines):
                        return [(i, j)]
                    if self.is_move_worth(lines):
                        self.possibilities.append((i, j))
        return self.possibilities
