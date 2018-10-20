print("hello world")

from array import *
from collections import namedtuple

fileName = 'board.txt'


class Game:
    Players = BLACK, WHITE = (1, 2)
    Player: int
    Action = namedtuple('Action', 'x, y')
    State = namedtuple('State', 'board, player, moves, utility')

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
        state.board[action.x - 1][action.y - 1] = state.player
        board = state.board.copy()
        board[action.x - 1][action.y - 1] = state.player
        moves = list(state.moves)
        moves.remove(action)
        return self.State(board, '1' if state.player == '0' else '0', moves, 0)

    def load_board(self, file=open(fileName, 'r')):
        first_line = file.readline()
        assert (len(first_line) >= 3)
        board_size = int(first_line[0])
        current_player = first_line[2]
        board = list(map(lambda s: list(filter(lambda c: c != '\n', list(s))), file.readlines()))
        moves = list()
        for i in range(0, len(board)):
            for j in range(0, len(board[i])):
                if board[i][j] == '0':
                    moves.append((i + 1, j + 1))
        file.close()
        return board, current_player, moves, 0
    def compute_utility


game = Game()
state = game.load_board()
print(state[0])
print(state)
