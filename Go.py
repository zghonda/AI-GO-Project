from array import *
from collections import namedtuple

fileName = 'board.txt'
infinity = float('inf')


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
            filter(lambda m: not (self.is_suicide(state.board, self.Action(m[0][1], m[0][1], m[1]))),
                   moves))
        return self.State(board, self.next_player(action), moves, self.compute_utility(state, action))

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
        return self.State(board, current_player,
                          list(
                              filter(lambda m: not (self.is_suicide(board, self.Action(m[0][1], m[0][1], m[1]))),
                                     moves)), 0)

    def alphabeta_cutoff_search(state, game, d=4, cutoff_test=None, eval_fn=None):
        """Search game to determine best action; use alpha-beta pruning.
        This version cuts off search and uses an evaluation function."""

        player = game.to_move(state)

        # Functions used by alphabeta
        def max_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            v = -infinity
            for a in game.actions(state):
                v = max(v, min_value(game.result(state, a),
                                     alpha, beta, depth + 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v

        def min_value(state, alpha, beta, depth):
            if cutoff_test(state, depth):
                return eval_fn(state)
            v = infinity
            for a in game.actions(state):
                v = min(v, max_value(game.result(state, a),
                                     alpha, beta, depth + 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        # Body of alphabeta_cutoff_search starts here:
        # The default test cuts off at depth d or at a terminal state
        cutoff_test = (cutoff_test or
                       (lambda state, depth: depth > d or
                                             game.terminal_test(state)))
        eval_fn = eval_fn or (lambda state: game.utility(state, player))
        best_score = -infinity
        beta = infinity
        best_action = None
        for a in game.actions(state):
            v = min_value(game.result(state, a), best_score, beta, 1)
            if v > best_score:
                best_score = v
                best_action = a
        return best_action

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
                return set([(i, j)])
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
        temp_board = board.copy()
        i, j, p = (action.i, action.j, action.player)
        old = temp_board[i][j]
        temp_board[i][j] = p
        num_liberties = len(self.get_liberties(temp_board, i, j))
        temp_board[i][j] = old
        return num_liberties == 0

    def compute_utility(self, state, action):
        list = [
            (i, j)
            for i in range(0, self.size)
            for j in range(0, self.size)
            if (state.board[i][j] != self.EMPTY and self.is_in_captured_group(state, i, j))
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
print(game.get_liberties(state.board, 1, 2))
print("board is ", state.board)
print(game.neighbors(state.board, 1, 2))
print(state.moves)
