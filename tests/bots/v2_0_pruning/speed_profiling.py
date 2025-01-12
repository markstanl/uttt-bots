import cProfile
import pstats

from bots.bot_match_up import BotMatchUp
from bots.eval.pm_eval.powell_merrill_evaluation import PowellMerrillEval
from bots.playable_bots.random_bot import RandomBot
from bots.playable_bots.v2_0_pruning.john_bot import JohnBotV2


def run_bot_match_up(num_games: int = 10):
    bot1 = RandomBot()
    bot2 = JohnBotV2(PowellMerrillEval())
    bot_match_up = BotMatchUp(bot1, bot2, print_games=True)
    bot_match_up.play(num_games)

    positions_evaluated = bot2.all_positions_evaluated
    print(positions_evaluated)
    print(sum(positions_evaluated) / len(positions_evaluated))


def main():
    profiler = cProfile.Profile()
    profiler.enable()

    run_bot_match_up(20)

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.strip_dirs()
    stats.sort_stats('cumtime')
    stats.print_stats(20)


if __name__ == '__main__':
    # 20 seconds for 1 game
    # 475 seconds for 20 games, ~24 seconds / game
    # 460 seconds with updated eval
    # 615 seconds, avg of 540 positions evaluated
    main()
