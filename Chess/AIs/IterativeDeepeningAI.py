"""
Author: Tucker SImpson
Date: 10/31/2022
"""

from AIs import AlphaBetaAI as ABAI
from AIs import MinimaxAI as MM
import Evaluator as Eval
import time

#TODO: Use information from previous layer to inform move ordering
class IterativeDeepeningAI:
    """
    Input: The maximum time ellapsed at which we will start a minimax search (with alpha-beta pruning) search at depth i
           max_player = false if the AI is playing black, = true if the AI is playing white
    """
    def __init__(self, max_start_time, max_player):
        self.max_start_time = max_start_time
        self.max_player = max_player
        self.evaluator = Eval.Evaluator(max_player)

    """
    Input: arrangement of the board
    Output: utility maximizing move for max_player based on minimax search
    """

    def choose_move(self, board):
        self.max_player = board.turn  # just in case

        # Keep track of the best move
        best_move = None

        # Start search time
        start_time = time.time()

        # Start at depth = 1
        depth = 0

        while time.time() - start_time < self.max_start_time:
            depth += 1

            # Search with alpha-beta pruning
            engineA = ABAI.AlphaBetaAI(depth, self.max_player)

            # Get best move from search at depth = depth
            ab_time = time.time()

            curr_moveA = engineA.choose_move(board)

            # Record the utility (for our interest)
            board.push(curr_moveA)
            curr_utility_A = self.evaluator.phase_1_evaluator(board)
            print("AlphaBeta recommending " + str(curr_moveA) + " at depth " + str(depth) + " for utility " + str(
                curr_utility_A))

            # Move found at the highest depth = the best move
            best_move = curr_moveA

            # Restore the board to input state
            board.pop()
            print("Time elapsed on AlphaBeta: " + str(time.time() - ab_time) + " seconds at depth " + str(depth) + "\n")

            ########### Testing to make sure AlphaBetaAI is working properly ###############
            # minimax_start = time.time()
            # engineB = MM.MinimaxAI(depth, self.max_player)
            # curr_moveB = engineB.choose_move(board)
            # board.push(curr_moveA)
            # curr_utility_B = self.evaluator.phase_1_evaluator(board)
            # print("Minimax recommending " + str(curr_moveB) + " at depth " + str(depth) + " for utility " + str(curr_utility_B))
            # print("Time elapsed on Minimax: " + str(time.time() - minimax_start) + " seconds.\n")
            # board.pop()

        print("\nIterativeDeepeningAI recommending " + str(best_move))

        return best_move
