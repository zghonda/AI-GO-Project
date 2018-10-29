from array import *
from collections import namedtuple

fileName = 'board.txt'

class Game:
    Action = namedtuple('Action', 'i, j, player')
    State = namedtuple('State', 'board, player, moves, utility')

    def __init__(self):
        self.size = 0
        self.EMPTY = '0'
        self.BLACK = '1'
        self.WHITE = '2'

    def to_move(self, state):
        return state.player

    def terminal_test(self, state):
        return state.utility != 0 or len(state.moves) == 0

    def utility(self, state, player):
        return state.utility if player == state.player else -state.utility

    def actions(self, state):
        return state.moves

    def result(self, state, action):
        if action not in state.moves:
            return state
        board = state.board.copy()
        board[action.i][action.j] = action.player
        moves = list(state.moves)
        moves.remove(action)
        moves = list(
            filter(lambda m: not (self.is_suicide(state, self.Action(m[0][1], m[0][1], m[1]))),
                   moves))
        return self.State(board, '1' if state.player == '2' else '0', moves, self.compute_utility(state, action))

    def load_board(self, file=open(fileName, 'r')):
        first_line = file.readline()
        assert (len(first_line) >= 3)
        self.size = int(first_line[0])
        current_player = first_line[2]
        board = list(map(lambda s: list(filter(lambda c: c != '\n', list(s))), file.readlines()))
        moves = list(map(lambda m:
                         ((m[0][0], m[0][1]), str(m[1])), [
                             ((i, j), p)
                             for p in range(1, 3)
                             for i in range(0, self.size)
                             for j in range(0, self.size)
                             if (board[i][j] == self.EMPTY)
                         ]))
        print(moves)
        file.close()
        state = self.State(board, current_player, moves, 0)
        return self.State(state.board, state.player,
                          list(
                              filter(lambda m: not (self.is_suicide(state, self.Action(m[0][1], m[0][1], m[1]))),
                                     moves)),
                          state.utility)

    def neighbors(self, state, i, j):
        surrounding = ((i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j))
        return map(lambda pos: (state.board[pos[0]][pos[1]], (pos[0], pos[1])),
                   filter(lambda coord: self.check_edge_overflow(coord[0], coord[1], self.size), surrounding))

    def get_liberties(self, state, i, j):

        def get_liberties_helper(self, state, i, j, traversed):
            """assert (self.check_edge_overflow(self, i, j, self.size))"""
            location = state.board[i][j]
            if location == self.EMPTY:
                return set([(i, j)])
            else:
                surroundings = [
                    (loc, (x, y))
                    for loc, (x, y) in self.neighbors(state, i, j)
                    if (loc == location or loc == self.EMPTY) and (x, y) not in traversed
                ]
                traversed.add((i, j))

                if surroundings:
                    return set.union(*[
                        get_liberties_helper(self, state, a, b, traversed)
                        for _, (a, b) in surroundings
                    ])
                else:
                    return set()

        return get_liberties_helper(self, state, i, j, set())

    def shift_to_game(self, value):
        return value + 1

    def shift_to_computer(self, value):
        return value - 1

    def check_edge_overflow(self, i, j, edge):
        return i in range(0, edge) and j in range(0, edge)

    def is_capture(self, state, i, j):
        return self.get_liberties(state, i, j)

    def is_suicide(self, state, action):
        # list are not immutable, solution has to be improved for esthetic reasons
        temp_board = state.board.copy()
        i, j, p = (action.i, action.j, action.player)
        old = temp_board[i][j]
        temp_board[i][j] = p
        num_liberties = len(self.get_liberties(self.State(temp_board, p, state.moves, state.utility), i, j))
        temp_board[i][j] = old
        return num_liberties == 0

    def compute_utility(self, state, action):
        list = [
            (i, j)
            for i in range(0, self.size)
            for j in range(0, self.size)
            if (state.board[i][j] != self.EMPTY and len(self.get_liberties(state, i, j)) == 0)
        ]
        assert (len(list) <= 1)
        if len(list) == 0:
            return 0
        else:
            (a, b) = list.pop()
            return -1 if state.player == state.board[a][b] else 1


game = Game()
state = game.load_board()
print("board is ", state.board)
print(game.get_liberties(state, 2, 1))
print(state.moves)
