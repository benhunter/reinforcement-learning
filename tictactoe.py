import abc
from enum import Enum
import logging
from pprint import pprint


DEBUG = False


class PositionState(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'

    def __str__(self) -> str:
        if self == PositionState.EMPTY:
            return ' '
        elif self == PositionState.X:
            return 'X'
        elif self == PositionState.O:
            return 'O'
        else:
            return ''


class BoardState:
    def __init__(self):
        self.board = [[PositionState.EMPTY for _ in range(3)] for _ in range(3)]
        self.turn = PositionState.X

    def board_as_tuple(self):
        return tuple(tuple(posn for posn in row) for row in self.board)


class Player(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass: type, /) -> bool:
        return (hasattr(subclass, 'make_move') and
            callable(subclass.make_move) and
            hasattr(subclass, 'get_name') and
            callable(subclass.get_name))

    def __init__(self, symbol: PositionState):
        self.symbol = symbol

    @abc.abstractmethod
    def choose_move(self, board_state: BoardState) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self):
        raise NotImplementedError


class HumanPlayer(Player):
    def choose_move(self, board_state) -> int:
        p = int(input('Enter position (1-9): '))
        return p

    def get_name(self) -> str:
        return 'Human'


class DumbPlayer(Player):
    # Try all moves 1-9 until a valid move is found
    def choose_move(self, board_state: BoardState) -> int:
        logging.debug(f'{self.symbol}\'s turn. Making a move...')
        for p in range(1, 10):
            logging.debug(f'Trying move {p}')
            x = (p - 1) % 3
            y = (p - 1) // 3
            logging.debug(f'x={x}, y={y}, board[{y}][{x}]={board_state.board[y][x]}')
            if board_state.board[y][x] == PositionState.EMPTY:
                logging.debug(f'Choosing move {p}')
                return p
        return 0

    def get_name(self) -> str:
        return 'Dumb - I play the next available position.'


class RLPlayer(Player):
    def __init__(self, symbol: PositionState):
        super().__init__(symbol)
        estimate_values = self.estimate_value()

    def estimate_value(self):
        board = BoardState()
        values = {}
        # pprint(board.board)
        # pprint(board.board_as_tuple())
        values[board.board_as_tuple()] = 0
        board.board[0][0] = PositionState.X
        values[board.board_as_tuple()] = 1
        pprint(values)
        raise NotImplementedError

    def choose_move(self, board_state: BoardState) -> int:
        return super().choose_move(board_state)

    def get_name(self):
        return super().get_name()


class TicTacToeGame:
    def __init__(self):
        self.board_state = BoardState()
        self.winner = PositionState.EMPTY

    def __str__(self) -> str:
        s = ''
        for y, row in enumerate(self.board_state.board):
            for x, position in enumerate(row):
                s += str(position)
                if x < 2:
                    s += '|'
            s += '\n'
            if y != 2:
                s += '-----\n'
        return s

    def __repr__(self) -> str:
        return ''

    def print_board(self):
        print(self)

    def print_turn(self):
        print(f'{self.board_state.turn}\'s turn')

    def make_move_at_xy(self, x, y):
        if x > 2 or x < 0 or y > 2 or y < 0:
            print('Invalid move')
            return
        if self.board_state.board[y][x] == PositionState.EMPTY:
            self.board_state.board[y][x] = self.turn
            self.turn = PositionState.X if self.turn == PositionState.O else PositionState.O
        else:
            print('Invalid move')

    def make_move_at(self, p) -> bool:
        logging.debug(f'{self.board_state.turn}\'s turn. Making a move...')
        logging.debug(f'p={p}')
        logging.debug(f'self.board={self.board_state.board}')
        if p < 1 or p > 9:
            print('Invalid move')
            return False
        x = (p - 1) % 3
        y = (p - 1) // 3
        if self.board_state.board[y][x] == PositionState.EMPTY:
            self.board_state.board[y][x] = self.board_state.turn
            self.board_state.turn = PositionState.X if self.board_state.turn == PositionState.O else PositionState.O
        else:
            print('Invalid move')
            return False
        return True

    def check_win(self):
        logging.debug(f'Checking for win')
        # check rows
        for row in self.board_state.board:
            if row[0] == row[1] == row[2] and row[0] != PositionState.EMPTY:
                self.winner = row[0]
                return True

        # check columns
        for col in range(3):
            if self.board_state.board[0][col] == self.board_state.board[1][col] == self.board_state.board[2][col] and self.board_state.board[0][col] != PositionState.EMPTY:
                self.winner = self.board_state.board[0][col]
                return True

        # check diagonals
        if self.board_state.board[0][0] == self.board_state.board[1][1] == self.board_state.board[2][2] and self.board_state.board[0][0] != PositionState.EMPTY:
            self.winner = self.board_state.board[0][0]
            return True

        if self.board_state.board[0][2] == self.board_state.board[1][1] == self.board_state.board[2][0] and self.board_state.board[0][2] != PositionState.EMPTY:
            self.winner = self.board_state.board[0][2]
            return True

        return False

    def check_tie(self):
        for row in self.board_state.board:
            for col in row:
                if col == PositionState.EMPTY:
                    return False
        return True

    def play(self, p1: Player, p2: Player):
        logging.debug(f'Playing game')
        print(f'Player 1: {p1.get_name()} is {p1.symbol}')
        print(f'Player 2: {p2.get_name()} is {p2.symbol}')
        assert p1.symbol != p2.symbol

        while self.check_win() == False and self.check_tie() == False:
            self.print_turn()
            move = p1.choose_move(self.board_state)
            self.make_move_at(move)
            self.print_board()

            if self.check_win() == True:
                print(f'{self.winner} won! Game Over')
                break
            if self.check_tie() == True:
                print('Tie! Game Over')
                break

            self.print_turn()
            move = p2.choose_move(self.board_state)
            self.make_move_at(move)
            self.print_board()

            if self.check_win() == True:
                print(f'{self.winner} won! Game Over')
                break
            if self.check_tie() == True:
                print('Tie! Game Over')
                break
            if DEBUG: input('Pausing for debug. Enter to continue.')


def main():
    RLPlayer(PositionState.X)
    return

    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    print(f'Tic Tac Toe')
    game = TicTacToeGame()
    logging.debug(game)
    p1 = DumbPlayer(PositionState.X)
    p2 = DumbPlayer(PositionState.O)
    game.play(p1, p2)


if __name__ == '__main__':
    main()
