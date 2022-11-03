"""
Author: Tucker SImpson
Date: 10/31/2022
"""

import random

import chess
from math import inf

import Evaluator as eval


class AlphaBetaAI:
    """
    Input: depth = depth of the game tree desired to search to
           player = true if white, false if black
    """
    def __init__(self, depth, player):
        self.depth = depth
        self.max_player = player
        self.evaluator = eval.Evaluator(self.max_player)
        self.num_calls = 0
        self.nodes_evaluated = 0

    """
    Input: state is the current arrangement of the board
    Output: best move for the player whose turn it is
    """
    def choose_move(self, board):
        # Recent counters
        self.num_calls = 0
        self.nodes_evaluated = 0

        # shuffle valid moves to avoid getting stuck in a continuous loop of the same moves
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Find the best move
        best_move = None
        max_utility = float('-inf')
        for move in moves:
            # Push the move to the board
            board.push(move)

            # Calculate the utility (opponent will take the move that minimizes our utility)
            curr_utility = self.min_move(board, 1)

            # Update the best move
            if curr_utility > max_utility:
                max_utility = curr_utility
                best_move = move

            # Reset the board
            board.pop()
        print("AlphaBetaAI recommending move " + str(best_move))
        print("Called a total of " + str(self.num_calls) + " times for maximum depth " + str(self.depth))
        print("Evaluated " + str(self.nodes_evaluated) + " nodes")
        return best_move

    """
    Input: arrangement of the board, current depth of the search, alpha, and beta (for alpha-beta pruning)
    Output: next legal move that maximizes our utility
    """
    def max_move(self, board, depth, alpha=float('-inf'), beta=float('inf')):
        self.num_calls += 1

        # Check whether we have reached the maximum depth or the end of the game
        if self.cutoff_test(board, depth):
            utility = self.evaluator.phase_1_evaluator(board)
            self.nodes_evaluated += 1
            return utility

        max_utility = float('-inf')

        # shuffle moves to avoid looping over the same set of moves
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Find the utility maximizing move
        for move in moves:
            # Update the board
            board.push(move)

            # Check if this is the best move we have found
            max_utility = max(max_utility, self.min_move(board, depth + 1, alpha, beta))

            # Return board back to input state
            board.pop()

            # Alpha-beta pruning
            if max_utility >= beta:
                return max_utility

            # Update alpha
            alpha = max(max_utility, alpha)

        # Return the maximum utility
        return max_utility

    """
    Input: arrangement of the board, current depth of the search, alpha, and beta (for alpha-beta pruning)
    Output: next legal move that maximizes our utility
    """
    def min_move(self, board, depth, alpha=float('-inf'), beta=float('inf')):
        self.num_calls += 1

        # Check if we have reached maximum depth or the end of the game
        if self.cutoff_test(board, depth):
            utility = self.evaluator.phase_1_evaluator(board)
            self.nodes_evaluated += 1
            return utility

        min_utility = float('inf')

        # shuffle moves to avoid looping over the same set of moves
        moves = list(board.legal_moves)
        random.shuffle(moves)

        # Look at legal moves
        for move in moves:
            # Update board
            board.push(move)

            # Check if we have found a new utility minimizing move
            min_utility = min(min_utility, self.max_move(board, depth + 1, alpha, beta))

            # Return the board back to input state
            board.pop()

            # Alpha-beta pruning
            if min_utility <= alpha:
                return min_utility

            # Update beta
            beta = min(beta, min_utility)

        # Return the minimum possible utility after the opponent makes their move
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
