from enum import Enum
import logging
import sys

DEBUG = False


class State(Enum):
	EMPTY = ' '
	X = 'X'
	O = 'O'

	def __str__(self):
		if self == State.EMPTY:
			return ' '
		elif self == State.X:
			return 'X'
		elif self == State.O:
			return 'O'


class Board:
	def __init__(self):
		self.board = [[State.EMPTY for _ in range(3)] for _ in range(3)]
		self.turn = State.X
		self.winner = State.EMPTY

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

	def __repr__(self) -> str:
		return ''

	def print_board(self):
		print(self)
		
	def print_turn(self):
		print(f'{self.turn}\'s turn')

	def make_move(self, x, y):
		if x > 2 or x < 0 or y > 2 or y < 0:
			print('Invalid move')
			return
		if self.board[y][x] == State.EMPTY:
			self.board[y][x] = self.turn
			self.turn = State.X if self.turn == State.O else State.O
		else:
			print('Invalid move')

	def make_move(self, p) -> bool:
		logging.debug(f'{self.turn}\'s turn. Making a move...')
		logging.debug(f'p={p}')
		logging.debug(f'self.board={self.board}')
		if p < 1 or p > 9:
			print('Invalid move')
			return false
		x = (p - 1) % 3
		y = (p - 1) // 3
		if self.board[y][x] == State.EMPTY:
			self.board[y][x] = self.turn
			self.turn = State.X if self.turn == State.O else State.O
		else:
			print('Invalid move')
			return False
		return True

	def check_win(self):
		logging.debug(f'Checking for win')
		# check rows
		for row in self.board:
			if row[0] == row[1] == row[2] and row[0] != State.EMPTY:
				self.winner = row[0]
				return True

		# check columns
		for col in range(3):
			if self.board[0][col] == self.board[1][col] == self.board[2][col] and self.board[0][col] != State.EMPTY:
				self.winner = self.board[0][col]
				return True

		# check diagonals
		if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != State.EMPTY:
			self.winner = self.board[0][0]
			return True

		if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != State.EMPTY:
			self.winner = self.board[0][2]
			return True

		return False

	def check_tie(self):
		for row in self.board:
			for col in row:
				if col == State.EMPTY:
					return False
		return True

	def play(self):
		while self.check_win() == False and self.check_tie() == False:
			self.print_turn()
			p = int(input('Enter position (1-9): '))
			self.make_move(p)
			self.print_board()
		print(f'{self.winner} won! Game Over')

	def play(self, p1, p2):
		logging.debug(f'Playing game')
		while self.check_win() == False and self.check_tie() == False:
			self.print_turn()
			p1.make_move(self)
			self.print_board()
			if self.check_win() == True:
				print(f'{self.winner} won! Game Over')
				break
			if self.check_tie() == True:
				print('Tie! Game Over')
				break
			self.print_turn()
			p2.make_move(self)
			self.print_board()
			if self.check_win() == True:
				print(f'{self.winner} won! Game Over')
				break
			if self.check_tie() == True:
				print('Tie! Game Over')
				break
			if DEBUG: input('Pausing for debug')


class Player:
	def __init__(self, symbol):
		self.symbol = symbol

	def make_move(self, board):
		pass


class HumanPlayer(Player):
	def make_move(self, board):
		p = int(input('Enter position (1-9): '))
		board.make_move(p)


class DumbPlayer(Player):
	# Try all moves 1-9 until a valid move is found
	def make_move(self, board: Board):
		logging.debug(f'{self.symbol}\'s turn. Making a move...')
		for p in range(1, 10):
			logging.debug(f'Trying move {p}')
			x = (p - 1) % 3
			y = (p - 1) // 3
			logging.debug(f'x={x}, y={y}, board[{y}][{x}]={board.board[y][x]}')
			if board.board[y][x] == State.EMPTY:
				logging.debug(f'Making move {p}')
				if board.make_move(p):
					break


def main():
	logging.basicConfig(level=logging.INFO)
	print(f'Tic Tac Toe')
	board = Board()
	logging.debug(board)
	p1 = DumbPlayer(State.X)
	p2 = DumbPlayer(State.O)
	board.play(p1, p2)


if __name__ == '__main__':
	main()