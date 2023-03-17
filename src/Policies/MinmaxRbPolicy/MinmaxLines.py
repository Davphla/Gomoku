class MinmaxLines:

    def __init__(self, map_size):
        self.map_size = map_size

    def get_horizonal_line(self, node, pos):
        """ Return horizonal line of 5 from a case in a board """
        start = max(0, pos[0] - 4)
        return [node.board[pos[1]][i + start] for i in range(9) if i + start < self.map_size]

    def get_vertical_line(self, node, pos):
        """ Return vertical line of 9 of a case in a board """
        start = max(0, pos[1] - 4)
        return [node.board[i + start][pos[0]] for i in range(9) if i + start < self.map_size]

    def get_diagonal_line(self, node, pos):
        """ Return diagonal line of 9 of a case in a board """
        start_x = max(0, pos[0] - 4)
        start_y = max(0, pos[1] - 4)
        return [node.board[i + start_y][i + start_x] for i in range(9) if
                i + start_x < self.map_size and i + start_y < self.map_size]

    def get_anti_diagonal_line(self, node, pos):
        """ Return anti-diagonal line of 9 of a case in a board """
        start_x = max(0, pos[0] - 4)
        start_y = min(self.map_size - 1, pos[1] + 4)
        line = [node.board[start_y - i][i + start_x] for i in range(9) if
                i + start_x < self.map_size and start_y - i >= 0]
        return line

    def get_lines_from_node(self, node, pos):
        """ Return vertical and horizonal, diagonal and anti-diagonal lines of 9 of a case in a board """
        lines = [self.get_horizonal_line(node, pos), self.get_vertical_line(node, pos),
                 self.get_diagonal_line(node, pos), self.get_anti_diagonal_line(node, pos)]
        return lines
