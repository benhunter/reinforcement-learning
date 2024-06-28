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

    def set_board_from_tuple(self, board_as_tuple):
        self.board = [[x for x in y] for y in board_as_tuple]

    def __repr__(self) -> str:
        return str(self.board_as_tuple())

    def __str__(self) -> str:
        s = ''
        for y, row in enumerate(self.board):
            for x, position in enumerate(row):
                s += str(position)
                if x < 2:
                    s += '|'
            s += '\n'
            if y != 2:
                s += '-----\n'
        return s

    def check_win(self) -> tuple[bool, PositionState]:
        logging.debug(f'Checking for win')
        win = False
        winner = PositionState.EMPTY

        # check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] != PositionState.EMPTY:
                win = True
                winner = row[0]
                return (win, winner)

        # check columns
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != PositionState.EMPTY:
                win = True
                winner = self.board[0][col]
                return (win, winner)

        # check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != PositionState.EMPTY:
            win = True
            winner = self.board[0][0]
            return (win, winner)

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != PositionState.EMPTY:
            win = True
            winner = self.board[0][2]
            return (win, winner)

        return (win, winner)

    def check_tie(self) -> bool:
        for row in self.board:
            for col in row:
                if col == PositionState.EMPTY:
                    return False
        return not self.check_win()[0]


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
        self.estimated_values = self.estimate_value()

    def estimate_value(self):
        board = BoardState()
        states = [board.board_as_tuple()]
        values = {}

        len_states = len(states)
        pprint(states)

        # Breadth-first search across all states
        while len(states) > 0:
            print(f'looping')
            current = states.pop()
            values[current] = 0.5

            board.set_board_from_tuple(current)
            for p in range(9):
                x = (p - 1) % 3
                y = (p - 1) // 3

                if board.board[y][x] == PositionState.EMPTY:
                    board.board[y][x] = PositionState.X
                    board_tuple = board.board_as_tuple()
                    states.append(board_tuple)

                    board.board[y][x] = PositionState.O
                    board_tuple = board.board_as_tuple()
                    states.append(board_tuple)

                    len_states += 2

        logging.debug(f'states found: {len_states}')
        logging.debug(values)
        print(values)
        logging.debug(f'len(values): {len(values)}')
        return values

    def choose_move(self, board_state: BoardState) -> int:
        return super().choose_move(board_state)

    def get_name(self):
        return super().get_name()


class TicTacToeGame:
    def __init__(self):
        self.board_state = BoardState()
        self.winner = PositionState.EMPTY

    def __str__(self) -> str:
        return str(self.board_state)

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

    def check_tie(self) -> bool:
        return self.board_state.check_tie()

    def play(self, p1: Player, p2: Player):
        logging.debug(f'Playing game')
        print(f'Player 1: {p1.get_name()} is {p1.symbol}')
        print(f'Player 2: {p2.get_name()} is {p2.symbol}')
        assert p1.symbol != p2.symbol

        while not self.board_state.check_win() and not self.check_tie():
            self.print_turn()
            move = p1.choose_move(self.board_state)
            self.make_move_at(move)
            self.print_board()

            if self.board_state.check_win() == True:
                print(f'{self.winner} won! Game Over')
                break
            if self.check_tie() == True:
                print('Tie! Game Over')
                break

            self.print_turn()
            move = p2.choose_move(self.board_state)
            self.make_move_at(move)
            self.print_board()

            if self.board_state.check_win() == True:
                print(f'{self.winner} won! Game Over')
                break
            if self.check_tie() == True:
                print('Tie! Game Over')
                break
            if DEBUG: input('Pausing for debug. Enter to continue.')


def main():
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
