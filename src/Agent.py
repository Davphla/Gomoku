import os
import sys
from enum import Enum

DEBUG = os.getenv('DEBUG', False)


class Agent:
    """
    Class defining the agent's relative observations
    """

    def __init__(self):
        self.game_state = self.GameState.NOT_MY_TURN
        self.reward = 0
        self.cmds = {"TURN": self.cmd_turn, "BOARD": self.cmd_board, "INFO": self.cmd_info, "END": self.cmd_end,
                     "START": self.cmd_start, "BEGIN": self.cmd_begin, "PRINT": self.cmd_print}
        self.settings = {"timeout_turn": "5", "timeout_match": None, "max_memory": "70000000",
                         "time_left": None, "game_type": "0", "rule": "1", "evaluate": None, "folder": None}
        self.map_size = 20
        self.board = None
        self.reset_board()

    def __del__(self):
        if DEBUG:
            print("Agent deleted", file=sys.stderr)

    def is_pos_free(self, pos):
        if self.board and 0 <= pos[0] < self.map_size and 0 <= pos[1] < self.map_size:
            return self.board[pos[1]][pos[0]] == 0
        return False

    def place_piece(self, pos, player):
        if self.is_pos_free(pos) and player in [1, 2]:
            self.board[pos[1]][pos[0]] = player
            return False
        return True

    def reset_board(self):
        self.board = [[0 for _ in range(self.map_size)] for _ in range(self.map_size)]

    def print_board(self):
        for i in self.board:
            print(i)

    def eval_state(self, cmd, data):
        """
        Evaluate the state of the agent and update its attributes
        :param cmd: command sent by the server
        :param data: data sent by the server
        """
        if cmd in self.cmds:
            return self.cmds[cmd](data)
        return False

    def cmd_start(self, value):
        if len(value) != 1:
            return True
        size = int(value[0])
        if size <= 0:
            return True
        self.map_size = size
        self.reset_board()
        return False

    def cmd_begin(self, value):
        self.game_state = self.GameState.MY_TURN
        return False

    def cmd_board(self, value):
        if not self.board:
            return True
        self.reset_board()
        for line in value:
            split_line = line.split(",")
            if len(split_line) != 3:
                return True
            x, y, player = map(int, split_line)
            if self.place_piece((x, y), player):
                return True
        self.game_state = self.GameState.MY_TURN
        return False

    def cmd_info(self, value):
        if len(value) != 2:
            return True
        key, val = value[0], value[1]
        self.settings[key] = val
        return False

    @staticmethod
    def cmd_end(value):
        exit(0)

    def cmd_turn(self, value):
        if not self.board or len(value) != 1:
            return True
        self.game_state = self.GameState.MY_TURN
        split_value = value[0].split(",")
        if len(split_value) == 2:
            x, y = map(int, split_value)
            return self.place_piece((x, y), self.PlayerState.ADVERSARY.value)
        return False

    def cmd_print(self, value):
        self.print_board()
        return False

    class GameState(Enum):
        MY_TURN = 0
        NOT_MY_TURN = 1
        WIN = 2
        LOSE = 3

    class PlayerState(Enum):
        EMPTY = 0
        IA = 1
        ADVERSARY = 2
