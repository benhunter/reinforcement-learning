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
    assert not board.check_win()

    board.board[0][0] = PositionState.X
    board.board[1][1] = PositionState.X
    board.board[2][2] = PositionState.X
    assert board.check_win()


def test_BoardState_check_tie():
    board = BoardState()
    assert not board.check_tie()

    board.board[0][0] = PositionState.X
    board.board[0][1] = PositionState.O
    board.board[0][2] = PositionState.X
    board.board[1][0] = PositionState.O
    board.board[1][1] = PositionState.X
    board.board[1][2] = PositionState.X
    board.board[2][0] = PositionState.O
    board.board[2][1] = PositionState.X
    board.board[2][2] = PositionState.O

    print(board)

    assert board.check_tie()


def test_TicTacToeGame_DumbPlayers():
    game = TicTacToeGame()
    p1 = DumbPlayer(PositionState.X)
    p2 = DumbPlayer(PositionState.O)

    assert str(game) == empty_board
    game.play(p1, p2)


def test_RLPlayer_init():
    RLPlayer(PositionState.X)
    RLPlayer(PositionState.O)
