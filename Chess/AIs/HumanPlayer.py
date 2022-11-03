import chess

class HumanPlayer():
    def __init__(self):
        print("Moves can be entered using four characters. For example, d2d4 moves the piece "
              "at d2 to d4.")
        self.max_player = True

    def choose_move(self, board):
        moves = list(board.legal_moves)

        uci_move = None

        while not uci_move in moves:
            print("Please enter your move: ")
            human_move = input()

            try:
                uci_move = chess.Move.from_uci(human_move)
            except:
                # illegal move format
                uci_move = None

            if uci_move not in moves:
                print("  That is not a legal move!")

        return uci_move

