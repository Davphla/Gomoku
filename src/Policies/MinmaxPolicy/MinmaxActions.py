import random
from ..RandomPolicy import RandomPolicy

class MinmaxActions:
    # Ideas of actions : Attack, Block

    def __init__(self, agent):
        self.agent = agent
        self.enemy_coord = []
        self.random = RandomPolicy(agent)
        self.possibilities = []

    def find_coord(self):
        for i in range(0, self.agent.map_size):
            for j in range(0, self.agent.map_size):
                if (self.agent.board[i][j] == 1 and self.enemy_coord.count([j, i]) <= 0):
                    self.enemy_coord.append([j, i])

    def find_vertical(self, pos):
        vertical = ""

        if (pos[1] < 4):
            start = 0
        else:
            start = pos[1] - 4

        i = 0
        while (i < 9 and i + start < self.agent.map_size):
            vertical += str(self.agent.board[i + start][pos[0]])
            i += 1

        return vertical

    def find_horizontal(self, pos):
        horizontal = ""

        if (pos[0] < 4):
            start = 0
        else:
            start = pos[0] - 4

        i = 0
        while (i < 9 and i + start < self.agent.map_size):
            horizontal += str(self.agent.board[pos[1]][i + start])
            i += 1

        return horizontal

    def find_diagonal1(self, pos):
        diagonal1 = ""

        if pos[0] < pos[1]:
            if (pos[0] < 4):
                start_x = 0
                start_y = pos[1] - pos[0]
            else:
                start_x = pos[0] - 4
                start_y = pos[1] - 4
        else:
            if (pos[1] < 4):
                start_y = 0
                start_x = pos[0] - pos[1]
            else:
                start_x = pos[0] - 4
                start_y = pos[1] - 4
        i = 0
        while (i < 9 and i + start_x < self.agent.map_size and i + start_y < self.agent.map_size):
            diagonal1 += str(self.agent.board[i + start_y][i + start_x])
            i += 1
        return diagonal1

    def find_diagonal2(self, pos):
        diagonal2 = ""

        if pos[1] < self.agent.map_size - 1 - pos[0]:
            if (pos[1] < 4):
                start_y = 0
                start_x = pos[0] + pos[1]
            else:
                start_x = pos[0] + 4
                start_y = pos[1] - 4
        else:
            if (self.agent.map_size - 1 - pos[0] < 4):
                start_x = self.agent.map_size - 1
                start_y = pos[1] - pos[0]
            else:
                start_x = pos[0] + 4
                start_y = pos[1] - 4

        i = 0
        while (i < 9 and start_x - i > 0 and i + start_y < self.agent.map_size):
            diagonal2 += str(self.agent.board[i + start_y][start_x - i])
            i += 1
        return diagonal2

    def check_priority(self, string):
        win = [["02222",  "20222", "22022", "22202", "22220"], 100000000]
        lose = [["01111", "10111", "11011", "11101", "11110"], 50000]

        fst_lose = [["11100", "11010", "11001", "10101", "01110", "10011", "01011", "00111", "10110", "01101"], 10000]
        fst_win = [["22200", "22020", "22002", "20202", "02220", "20022", "02022", "00222", "20220", "02202"], 2000]

        snd_win = [["22000", "20200", "20020", "20002", "02002", "00202", "00022", "02200", "00220", "02020"], 500]
        snd_lose = [["11000", "10100", "10010", "10001", "01001", "00101", "00011", "01100", "00110", "01010"], 200]

        trd_win = [["20000", "02000", "00200", "00020", "00002"], 50]
        trd_lose = [["10000", "01000", "00100", "00010", "00001"], 50]

        prios = [win, lose, fst_lose, fst_win, snd_win, snd_lose, trd_win, trd_lose]

        for prio in prios:
            for i in range(0, len(prio[0])):
                if (string.find(prio[0][i]) != -1):
                    return prio[1]
        return 0

    def check_possibilities(self, object):
        if (len(self.possibilities) == 0):
            return False
        for i in range(0, len(self.possibilities)):
            if (self.possibilities[i][0] == object[0] and self.possibilities[i][1] == object[1]):
                self.possibilities[i][2] += object[2]
                return True
        return False

    def checker(self):
        self.possibilities = []
        for y in range(0, self.agent.map_size):
            for x in range(0, self.agent.map_size):
                if (self.agent.is_pos_free([x, y])):
                    self.possibilities.append([[x, y], self.check_priority(self.find_vertical([x, y])) + self.check_priority(self.find_horizontal([x, y])) + self.check_priority(self.find_diagonal1([x, y])) + self.check_priority(self.find_diagonal2([x, y]))])

    def check_position(self):
        self.possibilities.sort(key=lambda x: x[1], reverse=True)
        maxWeight = self.possibilities[0][1]
        self.possibilities = list(filter(lambda x: (x[1] == maxWeight), self.possibilities))
        return self.possibilities[random.randint(0, len(self.possibilities) - 1)][0]

    def gestion(self):
        # Implémentation IA
        self.find_coord()
        # print(self.enemy_coord)

        if len(self.enemy_coord) == 1:
            return self.random.action.random_around_enemy(self.enemy_coord[0][0], self.enemy_coord[0][1])

        check = self.checker()

        if len(self.possibilities) != 0:
            pos = self.check_position()
            self.agent.place_piece(pos, 1)
            # print(self.possibilities)
            # self.agent.print_board()
            return pos

        return self.random.action.random_move()
