# BotHarmon
A chess AI built in Python that utilizes Minimax search and a static evaluator, optimized with alpha-beta pruning, lazy evaluation, move-ordering, and transposition tables.

## How it works

Chess can be conceptualized as a game tree, where each node signifies a move made by a player. Initially, White makes a decision, leading to a progression down the game tree. Subsequently, Black takes its turn, progressing further, and so forth. The terminal nodes within this game tree symbolize conclusive states of the game, such as Player 1 winning, Player 2 winning, or a tie (stalemate). This visualization method can be applied to various games. Take, for example, tic-tac-toe: the first move offers 9 options, the second move reduces the options to 8, the third to 7, and so on. Consequently, it is feasible to conclude that there are at most 9! possible game states in tic-tac-toe. Due to its relatively constrained decision space, tic-tac-toe qualifies as a "solved" game. We can systematically examine all potential moves from a given node and select the move that yields the highest utility, assuming both players employ optimal strategies.  

However, chess presents a substantially larger game and decision space. The number of conceivable board positions in chess is on the order of $10^{43}$, rendering the comprehensive enumeration of all potential positions through the game tree practically impossible. Instead, we still employ this game tree framework, but only delve a few layers deep. Furthermore, we navigate this tree by endeavoring to make moves that optimize our utility, all while presuming that our opponent will do the same.  

Nevertheless, the question arises: how do we gauge utility in a game if we are unable to traverse the tree to reach terminal states? To address this issue, a static evaluator is employed to estimate a player's utility based on their current position. A rudimentary utility heuristic function might solely consider material, whereas more advanced evaluators incorporate factors like piece positioning, development, mobility, and a multitude of other insights that humans have gleaned through years of studying chess to distinguish favorable positions from unfavorable ones. In this manner, by navigating the game tree to a shallow depth and employing an evaluation function to gauge position quality, a chess bot is empowered to play at a high level.  

### Minimax Search
<p align="center">
  <img width="406" alt="MiniMax Search" src="https://github.com/blackbeard6/BotHarmon/assets/103332396/ad6ca240-4550-4504-8062-2ec3e5f099f1">
</p">  

MiniMax search stands as a prevalent backtracking algorithm employed for enumerating and predicting potential states within a two-player game. It operates on the fundamental premise that both players are determined to secure victory. To illustrate, consider its application in a chess game. MiniMax search functions by traversing the game tree to a specified depth or until a terminal state is reached. At this juncture, it assesses the strength of each player's position by leveraging an evaluation function.  

In this process, maximum layers within the game tree correspond to the moves executed by the AI, while minimum layers correspond to the decisions enacted by the opponent. The AI selects the move that promises the highest utility when both players adhere to perfect gameplay, a definition contingent on the specific characteristics of our evaluation function, which informs the decision-making process in this context.

### Alpha-Beta Pruning

This optimization streamlines our Minimax search, preventing unnecessary exploration of implausible game states. It achieves this by halting the evaluation of a move as soon as it uncovers a single outcome indicating that the move is inferior to a previously analyzed one, all while enhancing search efficiency without impacting the ultimate result.

### Evaluation function

The current evaluation is centered around material; in general it awards higher utility to the player who has a higher quantity and quality of pieces on the board. Additionally, it accounts for the development of certain pieces, and has certain attributes of strong positions to look for, such as knight outposts, bishop pairs, a pawn-shield in front of the king, and more.


### Roadmap

Optimize performance on three fronts: (1) Speed up the search so we can traverse the game tree to a higher depth; (2) Improve our evaluation function to hard-code more intuition into the algorithm; and (3) Improve the average speed of the evaulation function. The roadmap for improving on these fronts is:
* [x] Implement alpha-beta pruning
* [x] Implement move-ordering to improve efficacy of alpha-beta pruning
* [ ] Parallelize game-tree search
* [ ] Incorporate transposition tables to memorize the utility corresponding to previously calculated game states
* [ ] Implement a lazy evaluation schema to minimize effort evaluating unrealistic positions

In addition,
* [ ] Incorporate an opening book
* [ ] Incorporate an end-game book

## How to run the program:
Use test_chess.py or gui_chess.py to see the AIs in action. The most sophisticated bots are the AlphaBetaAIv2 and the 
IterativeDeepeningAIv2. To run either, input the desired depth you want the AI to run minimax to, and also input the
color that the AI is playing for (input true for white and false if you want the AI to play black). You can play against
the AI using HumanPlayer() in test_chess.py, and gui_chess.py is best used to watch the bots play each other.
