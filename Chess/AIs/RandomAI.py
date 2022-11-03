#import chess
import random
from time import sleep

class RandomAI():
    # side = 1 or 2
    def __init__(self):
        pass

    def choose_move(self, board):
        moves = list(board.legal_moves)
        move = random.choice(moves)
        # sleep(1)   # I'm thinking so hard.
        print("Random AI recommending move " + str(move))

        pieces = []
        for i in range(0, 64):
            if board.piece_at(i):
                pieces.append(board.piece_at(i))

        # print("Playing for: " + str(board.turn))

        strength = 0
        for piece in pieces:
            side = 1
            if piece.color != board.turn: # assume for now that the AI plays white -- NEED TO FIX!EYC8
                side = -1

            # piece is a pawn
            if piece.piece_type == 1:
                strength += 1 * side
            # piece is a bishop or a knight
            elif piece.piece_type == 2 or piece.piece_type == 3:
                strength += 3 * side
            # piece is a rook
            elif piece.piece_type == 4:
                strength += 5 * side
            # piece is a queen
            elif piece.piece_type == 5:
                strength += 9 * side
            # piece is a king
            else:
                strength += 200 * side

        print("Evaluation result: " + str(strength))

        return move
