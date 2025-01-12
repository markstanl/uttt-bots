import cProfile
import pstats

from bots.bot_match_up import BotMatchUp
from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
from bots.playable_bots.random_bot import RandomBot
from bots.playable_bots.v1_minimax.minimax import Minimax2


def run_bot_matchup(num_games: int = 10):
    bot1 = RandomBot()
    bot2 = Minimax2(PowellMerrillEval())
    bot_match_up = BotMatchUp(bot1, bot2, print_games=True)
    bot_match_up.play(num_games)


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    run_bot_matchup(1)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumtime')
    stats.print_stats(20)


if __name__ == '__main__':
    # 143 seconds for 1 game
    main()
