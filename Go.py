print("hello world")

import fileinput

fileName = 'board.txt'

class Game:
    Players = BLACK, WHITE = (1, 2)
    Action = (Players, int, int)
    State = tuple()
    board_size : int

    def to_move(self, state: State):
        return

    def terminal_test(self, state: State):
        return

    def utility(self, s: State, player):
        return

    def actions(self, s: State):
        return

    def result(self, s: State, a: Action):
        return

    def load_board(self, file=open(fileName, 'r')):
        firstLine = file.readline()
        assert(len(firstLine)>=3)
        board_size = firstLine[0]
        current_player = firstLine[2]
        board = list(map(lambda s : list(filter(lambda c : c!='\n' ,list(s))),file.readlines()))
        file.close()
        return (board,current_player,board_size)



game = Game()
game.load_board()
