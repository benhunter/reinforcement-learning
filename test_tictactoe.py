import pytest

from tictactoe import BoardState, TicTacToeGame, DumbPlayer, PositionState, RLPlayer


empty_board = ''' | | 
-----
 | | 
-----
 | | 
'''


def test_BoardState_repr():
    new_board = BoardState()
    changed_board = BoardState()
    changed_board.board[0][0] = PositionState.X
    assert repr(new_board) != repr(changed_board)


def test_BoardState_str():
    assert str(BoardState()) == empty_board


def test_BoardState_check_win():
    board = BoardState()
    assert board.check_win() == False


@pytest.mark.xfail(reason="Not implemented yet")
def test_BoardState_check_tie():
    assert False


def test_TicTacToeGame_DumbPlayers():
    game = TicTacToeGame()
    p1 = DumbPlayer(PositionState.X)
    p2 = DumbPlayer(PositionState.O)

    assert str(game) == empty_board
    game.play(p1, p2)


def test_RLPlayer_init():
    RLPlayer(PositionState.X)
    RLPlayer(PositionState.O)
