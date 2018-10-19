print("hello world")

from array import *

fileName = 'board.txt'


class Game:
    Players = BLACK, WHITE = (1, 2)
    Player: int

    Action = (Players, int, int)
    State = tuple(list,Player,)


    def to_move(self, state: State):
        return state

    def terminal_test(self, state:State):
        board = state[0]

        for i in board :
            for j in board[i] :
                player = board[i][j]
                if(player != 0 &&   )
        return

    def utility(self, s: State, player):
        return

    def actions(self, s: State):
        return

    def result(self, s: State, a: Action):
        return

    def load_board(self, file=open(fileName, 'r')):
        first_line = file.readline()
        assert (len(first_line) >= 3)
        board_size = int(first_line[0])
        current_player = first_line[2]
        board = list(map(lambda s: list(filter(lambda c: c != '\n', list(s))), file.readlines()))
        file.close()
        return board, current_player, board_size

    board_size = load_board()[2]


game = Game()
game.load_board()
