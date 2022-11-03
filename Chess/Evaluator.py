"""
Author: Tucker SImpson
Date: 10/31/2022
"""
class Evaluator:
    # --------------CONSTANTS-----------
    DOUBLED_PAWN_VALUE = .9
    ROOK_PAWN_VALUE = .85
    EDGE_INDICES = {0, 8, 16, 24, 32, 40, 48, 56, 7, 15, 23, 31, 39, 47, 55, 63}
    ROOK_ON_OPEN_FILE_BONUS = .16
    ROOK_ON_SEMI_OPEN_FILE_BONUS = .08
    VALUE_RATE_OF_CHANGE = .005
    OUTPOST_BONUS = .10
    PAIR_BONUS = .1
    PAWN_SHIELD_BONUS = .05

    """
    Input: max_player = true if we are evaluating utility with respect to black, = false otherwise
    """
    def __init__(self, max_player):
        self.max_player = max_player

    """Gets the file index of the square where ``0`` is the a-file."""
    @staticmethod
    def square_file(square) -> int:
        return square & 7

    """Gets the rank index of the square where ``0`` is the first rank."""
    @staticmethod
    def square_rank(square) -> int:
        return square >> 3

    """
    Input: Board state
    Output: Rough utility estimation wrt max_player using material and positional cues
    """
    def phase_1_evaluator(self, board):
        num_pieces = 0  # proxy for our stage in the game

        # Piece counters
        friendly_bishops = 0
        friendly_knights = 0
        friendly_pawns = 0
        friendly_rooks = 0

        enemy_bishops = 0
        enemy_knights = 0
        enemy_pawns = 0
        enemy_rooks = 0

        # Track where our pawns, knights, and rooks are
        friendly_pawn_file_set = {-1}
        enemy_pawn_file_set = {-1}

        # Knight coordinates:
        friendly_knight_locs = []
        enemy_knight_locs = []

        friendly_rook_file_list = []
        enemy_rook_file_list = []

        strength = 0

        # Material evaluation
        for i in range(0, 64):
            # If we have a piece, evaluate it
            if board.piece_at(i):
                num_pieces += 1
                piece = board.piece_at(i)

                # Figure out what side the piece is playing for
                side = 1
                if piece.color != self.max_player:
                    side = -1

                # Piece is a pawn
                if piece.piece_type == 1:
                    weight = 1

                    # Less weight for rook's pawn
                    if i in self.EDGE_INDICES:
                        weight = self.ROOK_PAWN_VALUE

                    if side == 1:
                        friendly_pawns += 1
                        # Punish doubled pawns
                        if i in friendly_pawn_file_set:
                            weight *= self.DOUBLED_PAWN_VALUE
                        else:
                            friendly_pawn_file_set.add(self.square_file(i))

                    else:

                        enemy_pawns += 1
                        # Punish doubled pawns
                        if i in enemy_pawn_file_set:
                            weight *= self.DOUBLED_PAWN_VALUE
                        else:
                            enemy_pawn_file_set.add(self.square_file(i))

                    strength += weight * side

                # piece is a knight
                elif piece.piece_type == 2:
                    if side == 1:
                        friendly_knights += 1
                        friendly_knight_locs.append(i)
                    else:
                        enemy_knights += 1
                        enemy_knight_locs.append(i)

                # piece is a bishop
                elif piece.piece_type == 3:
                    if side == 1:
                        friendly_bishops += 1
                    else:
                        enemy_bishops += 1

                # piece is a rook
                elif piece.piece_type == 4:
                    if side == 1:
                        friendly_rooks += 1
                        friendly_rook_file_list.append(self.square_file(i))
                    else:
                        enemy_rooks += 1
                        enemy_rook_file_list.append(self.square_file(i))

                # piece is a queen
                elif piece.piece_type == 5:
                    strength += 9 * side

                # piece is a king
                else:
                    strength += 200 * side

                    # Check for pawn shield
                    if piece.color:
                        if board.piece_at(i + 8) and board.piece_at(i + 8).piece_type == 1:
                            if piece.color == self.max_player:
                                strength += self.PAWN_SHIELD_BONUS
                            else:
                                strength -= self.PAWN_SHIELD_BONUS
                    else:
                        if board.piece_at(i - 8) and board.piece_at(i - 8).piece_type == 1:
                            if piece.color == self.max_player:
                                strength += self.PAWN_SHIELD_BONUS
                            else:
                                strength -= self.PAWN_SHIELD_BONUS

        # Handle knight evaluation -- decrease value as the number of pawns decreases
        strength += (friendly_knights - enemy_knights) * (
                3 - (self.VALUE_RATE_OF_CHANGE * (16 - (friendly_pawns + enemy_pawns))))

        # Check for outpost
        outpost_bonus = 0
        for loc in friendly_knight_locs:
            # Identify if it is in the center
            if 6 > self.square_rank(loc) > 1:
                if 7 > self.square_file(loc) > 0:
                    # check if we have pawn support
                    left_support_loc = loc - 9
                    right_support_loc = loc - 7
                    if board.piece_at(left_support_loc) and board.piece_at(left_support_loc).piece_type == 1 and \
                            board.piece_at(left_support_loc).color == self.max_player \
                            or board.piece_at(right_support_loc) and \
                            board.piece_at(right_support_loc).piece_type == 1 and \
                            board.piece_at(right_support_loc).color == self.max_player:

                        outpost_bonus += self.OUTPOST_BONUS

        for loc in enemy_knight_locs:
            # Identify if it is in the center
            # TODO: Make sure this isn't what's causing aggressive knight development
            if 6 > self.square_rank(loc) > 1:
                if 7 > self.square_file(loc) > 0:
                    # check if we have pawn support
                    left_support_loc = loc + 9
                    right_support_loc = loc + 7
                    if board.piece_at(left_support_loc) and board.piece_at(left_support_loc).piece_type == 1 \
                            and board.piece_at(left_support_loc).color != self.max_player or \
                            board.piece_at(right_support_loc) and \
                            board.piece_at(right_support_loc).piece_type == 1 and \
                            board.piece_at(right_support_loc) != self.max_player:

                        outpost_bonus -= self.OUTPOST_BONUS

        strength += outpost_bonus

        # Handle bishop evaluation
        # Provide a bonus for pair of bishops
        pair_bonus = 0
        if friendly_bishops > 1:
            pair_bonus += self.PAIR_BONUS
        if enemy_bishops > 1:
            pair_bonus -= self.PAIR_BONUS
        strength += 3 * (friendly_bishops - enemy_bishops)
        strength += pair_bonus

        # Handle rook evaluation
        open_file_bonus = 0
        for file in friendly_rook_file_list:
            if file not in friendly_pawn_file_set:
                if file not in enemy_pawn_file_set:
                    open_file_bonus += self.ROOK_ON_OPEN_FILE_BONUS
                else:
                    open_file_bonus += self.ROOK_ON_SEMI_OPEN_FILE_BONUS

        for file in enemy_rook_file_list:
            if file not in enemy_pawn_file_set:
                if file not in friendly_pawn_file_set:
                    open_file_bonus -= self.ROOK_ON_OPEN_FILE_BONUS
                else:
                    open_file_bonus -= self.ROOK_ON_SEMI_OPEN_FILE_BONUS

        strength += open_file_bonus
        strength += (friendly_rooks - enemy_rooks) * (
                5 + self.VALUE_RATE_OF_CHANGE * (16 - (friendly_pawns + enemy_pawns)))

        return strength
