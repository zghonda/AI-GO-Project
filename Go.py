from array import *
from collections import namedtuple
from copy import *
from itertools import *

fileName = 'board.txt'
infinity = float('inf')


class Game:
    # Action = tuple('i, j, player')
    state = namedtuple('state', 'board, player, moves')

    def __init__(self):
        self.size = 0
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2

    def to_move(self, state):
        return state.player

    def terminal_test(self, state):
        ''' Return True if state is terminal '''
        if self.check_if_draw(state): return True
        # One piece has no liberties
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self.is_in_captured_group(state.board, i, j):
                    return True
        return False

    def utility(self, state, player):
        if self.terminal_test(state):
            # Check if draw
            if self.check_if_draw(state): return 0
            for i in range(0, self.size):
                for j in range(0, self.size):
                    if self.is_in_captured_group(state.board, i, j):
                        if state.board[i][j] == player: return -1
                        return 1
        return 99

    def check_if_draw(self, state):
        '''' Returns True or False whether it's a draw '''

        return len(self.generate_moves(state.board)) == 0
        #
        # for certain_player in range(1, 3):
        #   count_moves = 0
        #  for i in range(0, len(state.moves)):
        #     if state.moves[i][0] == certain_player: count_moves += 1
        # if count_moves == 0: return True
        # return False

    def actions(self, state):
        return list(filter(lambda m: m[0] == state.player, state.moves))

    def result(self, state, action):
        board = self.apply_action(state, action)

        if action in state.moves:
            print("yes")
            print(action)
            state.moves.remove(action)

        player = action[0]
        moves = self.remove_suicide(board, state.moves, player)
        return self.state(board, self.next_player(player), moves)

    def apply_action(self, board, action):
        board = deepcopy(board)
        (p, i, j) = (action[0], self.shift_to_computer(action[1]), self.shift_to_computer(action[2]))
        board[i][j] = p
        return board

    def remove_suicide(self, board, moves, player):
        # <0 because result flips the player turn
        return list(
            filter(lambda m: not (self.is_suicide(board, m)
                                  and not (
                            self.utility(self.state(self.apply_action(board, m), player, moves), player) == 1)),
                   moves))

    # def load_board(self, fileName):
    # file = open(fileName, 'r')
    def load_board(self, file=open(fileName, 'r')):
        first_line = file.readline()
        assert (len(first_line) >= 3)
        self.size = int(first_line[0])
        current_player = int(first_line[2])
        board = list()
        for line in file.readlines():
            board.append(list(map(lambda char: int(char), list(filter(lambda c: c != '\n', list(line))))))

        moves = self.generate_moves(board)
        print(moves)
        moves = self.remove_suicide(deepcopy(board), moves, current_player)
        print(moves)
        file.close()
        # Put terminal_test in print
        # print(self.terminal_test(self.result(self, state, (1, 1, '1'))))

        return self.state(board, current_player, moves)

    def generate_moves(self, board):
        return [
            (p, self.shift_to_game(i), self.shift_to_game(j))
            for p in range(1, 3)
            for i in range(0, self.size)
            for j in range(0, self.size)
            if (board[i][j] == self.EMPTY)
        ]

    def neighbors(self, board, i, j):
        surrounding = ((i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j))
        return list(map(lambda pos: (board[pos[0]][pos[1]], (pos[0], pos[1])),
                        filter(lambda coord: self.check_edge_overflow(coord[0], coord[1], self.size), surrounding)))

    def next_player(self, player):
        return self.BLACK if player == self.WHITE else self.WHITE

    def get_liberties(self, board, i, j):
        def get_liberties_helper(self, board, i, j, traversed):
            """assert (self.check_edge_overflow(self, i, j, self.size))"""
            location = board[i][j]
            if location == self.EMPTY:
                return {(i, j)}
            else:
                surroundings = [
                    (loc, (a, b))
                    for loc, (a, b) in self.neighbors(board, i, j)
                    if (loc == location or loc == self.EMPTY) and (a, b) not in traversed
                ]
                traversed.add((i, j))

                if surroundings:
                    return set.union(*[
                        get_liberties_helper(self, board, a, b, traversed)
                        for _, (a, b) in surroundings
                    ])
                else:
                    return set()

        return get_liberties_helper(self, board, i, j, set())

    def shift_to_game(self, value):
        return value + 1

    def shift_to_computer(self, value):
        return value - 1

    def check_edge_overflow(self, i, j, edge):
        return i in range(0, edge) and j in range(0, edge)

    def is_in_captured_group(self, board, i, j):
        return len(self.get_liberties(board, i, j)) == 0

    def is_suicide(self, board, action):
        # list are not immutable, solution has to be improved for esthetic reasons
        temp_board = deepcopy(board)
        p, i, j = (action[0], self.shift_to_computer(action[1]), self.shift_to_computer(action[2]))
        temp_board[i][j] = p
        return self.is_in_captured_group(temp_board, i, j)

    def evalfn(self, state, player):
        my_conglomerates = []
        enemy_conglomerates = []
        board_pos = [self.size + 1][self.size + 1]
        # Not sure about max
        # my_pieces = list(map(lambda pos: state.board[pos[0]][pos[1]] == player, board_pos))
        my_pieces = [[(i, j), "i"]
                     for i in range(0, self.size)
                     for j in range(0, self.size)
                     if (state.board[i][j] == player)
                     ]
        # enemy_pieces = list(map(lambda pos: state.board[pos[0]][pos[1]] == str((int(player)%2)+1), board_pos))
        enemy_pieces = [[(i, j), "i"]
                        for i in range(0, self.size)
                        for j in range(0, self.size)
                        if (state.board[i][j] == str((int(player) % 2) + 1))
                        ]

        for i in range(0, len(my_pieces)):
            if (my_pieces[i][1] == "i"):
                neighbours = game.neighbors(state.board, my_pieces[i][0][0], my_pieces[i][0][1])
                for j in range(0, len(neighbours)):
                    for z in range(0, len(my_conglomerates)):
                        if (neighbours[j][1] in my_conglomerates[z]):
                            my_pieces[i][1] = z
                            my_conglomerates[z].append(my_pieces[i][0])
            if (my_pieces[i][1] == "i"):
                my_pieces[i][1] = len(my_conglomerates)
                my_conglomerates.append([my_pieces[i][0]])

        for i in range(0, len(enemy_pieces)):
            if (enemy_pieces[i][1] == "i"):
                neighbours = game.neighbors(state.board, enemy_pieces[i][0][0], enemy_pieces[i][0][1])
                for j in range(0, len(neighbours)):
                    for z in range(0, len(enemy_conglomerates)):
                        if (neighbours[j][1] in enemy_conglomerates[z]):
                            enemy_pieces[i][1] = z
                            enemy_conglomerates[z].append(enemy_pieces[i][0])
            if (enemy_pieces[i][1] == "i"):
                enemy_pieces[i][1] = len(enemy_conglomerates)
                enemy_conglomerates.append([enemy_pieces[i][0]])

        my_liberties = []
        for i in range(0, 3):
            count = 0
            for j in range(0, len(my_conglomerates)):
                if (len(game.get_liberties(state.board, my_conglomerates[j][0][0],
                                           my_conglomerates[j][0][1])) == i + 1):
                    count = count + 1
            my_liberties.append(count)
        enemy_liberties = []
        for i in range(0, 3):
            count = 0
            for j in range(0, len(enemy_conglomerates)):
                if (len(game.get_liberties(state.board, enemy_conglomerates[j][0][0],
                                           enemy_conglomerates[j][0][1])) == i + 1):
                    count += 1
            enemy_liberties.append(count)
        my_liberties[2] = my_liberties[2] / 2
        enemy_liberties[2] = enemy_liberties[2] / 2
        print(my_liberties)
        print(enemy_liberties)
        Eval = 0
        for i in range(0, 3):
            Eval += my_liberties[i] - enemy_liberties[i]
        if Eval < 0:
            return Eval - 2
        if Eval >= 0:
            return Eval + 2


game = Game()
state = game.load_board()

print("board is ", state.board)
print(state)
board = game.apply_action(state.board, (1, 2, 4))
print(board)
