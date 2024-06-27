from tictactoe import TicTacToeGame, DumbPlayer, PositionState


def test_TicTacToeGame_DumbPlayers():
    game = TicTacToeGame()
    p1 = DumbPlayer(PositionState.X)
    p2 = DumbPlayer(PositionState.O)

    game.play(p1, p2)
