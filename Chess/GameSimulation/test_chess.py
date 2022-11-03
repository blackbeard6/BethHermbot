# pip3 install python-chess


from AIs.RandomAI import RandomAI
from AIs.HumanPlayer import HumanPlayer
from AIs.AlphaBetaAI import AlphaBetaAI
from NextGen.AlphaBetaAIv2 import AlphaBetaAIv2
from NextGen.IterativeDeepeningAIv2 import IterativeDeepeningAIv2
from AIs.MinimaxAI import MinimaxAI
from GameSimulation.ChessGame import ChessGame
from AIs.IterativeDeepeningAI import IterativeDeepeningAI

# player1 = MinimaxAI(3)
# player1 = AlphaBetaAI(3)
# player1 = IterativeDeepeningAI(5, True)
player1 = IterativeDeepeningAIv2(30, True)
# player1 = MinimaxAI(2, True)
player2 = AlphaBetaAI(2, False)
# player2 = MinimaxAI(3)
# player2 = RandomAI()

# how do we know which is white, which is black?
game = ChessGame(player1, player2)

while not game.is_game_over():
    print(game)
    game.make_move()


#print(hash(str(game.board)))
