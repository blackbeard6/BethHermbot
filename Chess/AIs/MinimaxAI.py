"""
Author: Tucker SImpson
Date: 10/31/2022
"""

import random

import chess
from math import inf
import Evaluator as eval

class MinimaxAI():
    num_calls = 0
    nodes_evaluated = 0

    """
    Input: depth = depth of the game tree desired to search to
           player = true if white, false if black
    """
    def __init__(self, depth, max_player):
        self.depth = depth
        self.max_player = False
        self.num_calls = 0
        self.nodes_evaluated = 0
        self.max_player = max_player
        self.evaluator = eval.Evaluator(max_player)

    """
    Input: state is the current arrangement of the board
    Output: best move for the player whose turn it is
    """
    def choose_move(self, board):
        self.max_player = board.turn
        self.num_calls = 0
        self.nodes_evaluated = 0

        # Get legal moves and shuffle
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Keep track of the best move
        best_move = None
        max_utility = float('-inf')

        # Check all legal moves
        for move in moves:
            # Update board
            board.push(move)

            # Get the utility of that move, assuming opponent minimizes our utility
            curr_utility = self.min_move(board, 1)

            # Check if we have found a new best move
            if curr_utility > max_utility:
                max_utility = curr_utility
                best_move = move

            # Return the board to its input state
            board.pop()

        print("MinimaxAI recommending move " + str(best_move))
        print("Called a total of " + str(self.num_calls) + " times for maximum depth " + str(self.depth))
        print("Evaluated " + str(self.nodes_evaluated) + " nodes")
        return best_move

    """
    Input: arrangement of the board, current depth of the search, alpha, and beta (for alpha-beta pruning)
    Output: next legal move that maximizes our utility
    """
    def max_move(self, board, depth):
        self.num_calls += 1

        # Check if we have reached the maximum depth or the game is over
        if self.cutoff_test(board, depth):
            utility = self.evaluator.phase_1_evaluator(board)
            self.nodes_evaluated += 1
            return utility

        # Keep track of the best move
        max_utility = float('-inf')

        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Check over all legal moves
        for move in moves:
            # Update the board
            board.push(move)

            # Check whether it is the best move we have seen
            max_utility = max(max_utility, self.min_move(board, depth + 1))

            # Return the board to its input state
            board.pop()

        return max_utility

    """
    Input: arrangement of the board, current depth of the search, alpha, and beta (for alpha-beta pruning)
    Output: next legal move that maximizes our utility
    """
    def min_move(self, board, depth):
        self.num_calls += 1

        # Check if the game is over or we have searched to the depth limit
        if self.cutoff_test(board, depth):
            utility = self.evaluator.phase_1_evaluator(board)
            self.nodes_evaluated += 1
            return utility

        # Keep track of the utility minimizing move
        min_utility = float('inf')
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Look at all legal moves
        for move in moves:
            # Update the board
            board.push(move)

            # Check if we have found a new utility minimizing move
            min_utility = min(min_utility, self.max_move(board, depth + 1))

            # Return the board to the input state
            board.pop()

        return min_utility

    """
    Input: Board
    Output: True if we have reached the end of the game, False otherwise
    """
    def terminal_test(self, board):
        if board.is_game_over():
            return True
        return False

    """
    Input: Board and current depth
    Output: True if we have reached the end of the game or the maximum depth, False otherwise
    """
    def cutoff_test(self, board, depth):
        if depth == self.depth:
            return True

        if self.terminal_test(board):
            return True

        return False