#!/usr/bin/env python3
import logging
from enum import Enum

logging.getLogger().setLevel(logging.INFO)


class RockPaperScissors(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class GameOutcome(Enum):
    LOSS = 0
    DRAW = 3
    WIN = 6

outcome_map: dict[str, GameOutcome] = {
    'X': GameOutcome.LOSS,
    'Y': GameOutcome.DRAW,
    'Z': GameOutcome.WIN
}

rps_map: dict[str, RockPaperScissors] = {
    'A': RockPaperScissors.ROCK,     'X': RockPaperScissors.ROCK,
    'B': RockPaperScissors.PAPER,    'Y': RockPaperScissors.PAPER,
    'C': RockPaperScissors.SCISSORS, 'Z': RockPaperScissors.SCISSORS
}

rps_outcome_map: dict[tuple[RockPaperScissors, RockPaperScissors], GameOutcome] = {
    (RockPaperScissors.ROCK, RockPaperScissors.ROCK): GameOutcome.DRAW,
    (RockPaperScissors.ROCK, RockPaperScissors.PAPER): GameOutcome.WIN,
    (RockPaperScissors.ROCK, RockPaperScissors.SCISSORS): GameOutcome.LOSS,
    (RockPaperScissors.PAPER, RockPaperScissors.ROCK): GameOutcome.LOSS,
    (RockPaperScissors.PAPER, RockPaperScissors.PAPER): GameOutcome.DRAW,
    (RockPaperScissors.PAPER, RockPaperScissors.SCISSORS): GameOutcome.WIN,
    (RockPaperScissors.SCISSORS, RockPaperScissors.ROCK): GameOutcome.WIN,
    (RockPaperScissors.SCISSORS, RockPaperScissors.PAPER): GameOutcome.LOSS,
    (RockPaperScissors.SCISSORS, RockPaperScissors.SCISSORS): GameOutcome.DRAW,
}

rps_choose_map: dict[tuple[RockPaperScissors,GameOutcome], RockPaperScissors] = {
    (RockPaperScissors.ROCK, GameOutcome.LOSS): RockPaperScissors.SCISSORS,
    (RockPaperScissors.ROCK, GameOutcome.DRAW): RockPaperScissors.ROCK,
    (RockPaperScissors.ROCK, GameOutcome.WIN): RockPaperScissors.PAPER,
    (RockPaperScissors.PAPER, GameOutcome.LOSS): RockPaperScissors.ROCK,
    (RockPaperScissors.PAPER, GameOutcome.DRAW): RockPaperScissors.PAPER,
    (RockPaperScissors.PAPER, GameOutcome.WIN): RockPaperScissors.SCISSORS,
    (RockPaperScissors.SCISSORS, GameOutcome.LOSS): RockPaperScissors.PAPER,
    (RockPaperScissors.SCISSORS, GameOutcome.DRAW): RockPaperScissors.SCISSORS,
    (RockPaperScissors.SCISSORS, GameOutcome.WIN): RockPaperScissors.ROCK,
}

part_one_value: int = 0
part_two_value: int = 0

with open('2022/2022-12-02.txt') as input_file:
    for input_line in input_file:
        input_line: str = input_line.strip()
        first, second = input_line.split(' ')
        opponent: RockPaperScissors = rps_map[first]
        you_part_one: RockPaperScissors = rps_map[second]
        outcome_part_one: GameOutcome = rps_outcome_map[opponent, you_part_one]
        part_one_value += you_part_one.value + outcome_part_one.value
        outcome_part_two: GameOutcome = outcome_map[second]
        you_part_two: RockPaperScissors = rps_choose_map[opponent, outcome_part_two]
        part_two_value += you_part_two.value + outcome_part_two.value

logging.info('part one: {}'.format(part_one_value))
logging.info('part two: {}'.format(part_two_value))