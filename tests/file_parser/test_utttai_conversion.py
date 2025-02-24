from ultimate_tic_tac_toe import Player, Move
from ultimate_tic_tac_toe.game import Game
from utttai_conversion import utttai_conversion

class TestUtttaiConversion:
    def setup_method(self):
        move_indices = [0, 1, 3, 2]
        self.expected_game = Game()
        for i, move in enumerate(move_indices):
            if i % 2 == 0:
                self.expected_game.push(Move(move, Player.X))
            else:
                self.expected_game.push(Move(move, Player.O))
        self.u3t_to_utttai_big_pairs = [(0, 6), (1, 7), (2, 8), (3, 3), (4, 4), (5, 5), (6, 0), (7, 1), (8, 2)]
        self.u3t_to_utttai_small_pairs = [(0, 60), (1, 61), (2, 62), (3, 69), (4, 70), (5, 71), (6, 78), (7, 79), (8, 80),
                               (9, 57), (10, 58), (11, 59), (12, 66), (13, 67), (14, 68), (15, 75), (16, 76), (17, 77),
                               (18, 54), (19, 55), (20, 56), (21, 63), (22, 64), (23, 65), (24, 72), (25, 73), (26, 74),
                               (27, 33), (28, 34), (29, 35), (30, 42), (31, 43), (32, 44), (33, 51), (34, 52), (35, 53),
                               (36, 30), (37, 31), (38, 32), (39, 39), (40, 40), (41, 41), (42, 48), (43, 49), (44, 50),
                               (45, 27), (46, 28), (47, 29), (48, 36), (49, 37), (50, 38), (51, 45), (52, 46), (53, 47),
                               (54, 6), (55, 7), (56, 8), (57, 15), (58, 16), (59, 17), (60, 24), (61, 25), (62, 26),
                               (63, 3), (64, 4), (65, 5), (66, 12), (67, 13), (68, 14), (69, 21), (70, 22), (71, 23),
                                (72, 0), (73, 1), (74, 2), (75, 9), (76, 10), (77, 11), (78, 18), (79, 19), (80, 20)]

    def test_small_u3t_to_utttai(self):
        for u3t_index, utttai_index in self.u3t_to_utttai_small_pairs:
            assert utttai_conversion.u3t_small_index_to_utttai_small_index(u3t_index) == utttai_index

    def test_small_utttai_to_u3t(self):
        for u3t_index, utttai_index in self.u3t_to_utttai_small_pairs:
            assert utttai_conversion.utttai_small_index_to_u3t_small_index(utttai_index) == u3t_index

    def test_big_index_conversion(self):
        for u3t_index, utttai_index in self.u3t_to_utttai_big_pairs:
            assert utttai_conversion.u3t_big_index_to_utttai_big_index(u3t_index) == utttai_index

        for u3t_index, utttai_index in self.u3t_to_utttai_big_pairs:
            assert utttai_conversion.utttai_big_index_to_u3t_big_index(utttai_index) == u3t_index
