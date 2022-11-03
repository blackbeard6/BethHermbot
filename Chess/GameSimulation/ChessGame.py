import chess


class ChessGame:
    def __init__(self, player1, player2):
        self.board = chess.Board()
        self.players = [player1, player2]

    def make_move(self):

        player = self.players[1 - int(self.board.turn)]
        move = player.choose_move(self.board)

        print(str(move))
        if move is None:
            print(self.board.outcome)
        else:
            self.board.push(move)  # Make the move
            # print(self.board.board_fen())

    def is_game_over(self):
        if self.board.is_game_over():
            print("Game over: " + self.board.result())
        return self.board.is_game_over()

    def __str__(self):

        column_labels = "\n----------------\na b c d e f g h\n"
        board_str =  str(self.board) + column_labels

        # did you know python had a ternary conditional operator?
        move_str = "White to move" if self.board.turn else "Black to move"

        return board_str + "\n" + move_str + "\n"
