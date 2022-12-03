#!/usr/bin/env python3
import logging
from typing import Iterable

logging.getLogger().setLevel(logging.INFO)

def FindCommonItems(*strs: str) -> str:
    # Would've like map() and itertools.reduce() here, but set.intersection winds up
    # underspecified in the reduce.
    sets: Iterable[set[str]] = map(set, strs)
    result: set[str] = next(sets)
    while True:
        try:
            result.intersection_update(next(sets))
        except StopIteration:
            break
    return ''.join(result)

def PriorityScoreChar(item: str) -> int:
    assert len(item) == 1
    if item.isupper():
        return 1 + 26 + ord(item) - ord('A')
    else:
        return 1 + ord(item) - ord('a')

with open('2022/2022-12-03.txt') as input_file:
    total_score_part_one: int = 0
    total_score_part_two: int = 0
    current_group: list[str] = []
    for input_line in input_file:
        items: str = input_line.strip()
        # Part One
        total_item_count: int = len(items)
        logging.debug("len = {}".format(total_item_count))
        first_items: str = items[:total_item_count//2]
        second_items: str = items[total_item_count//2:]
        logging.debug("{}  |  {}".format(first_items, second_items))
        commons: str = FindCommonItems(first_items, second_items)
        logging.debug("common = {}".format(commons))
        score: int = PriorityScoreChar(commons)
        total_score_part_one += score
        logging.debug(f"score = {score}")
        # Part Two
        current_group.append(items)
        if len(current_group) == 3:
            commons: str = FindCommonItems(*current_group)
            score: int = PriorityScoreChar(commons)
            total_score_part_two += score
            current_group = []
            
    logging.info(f"total score part one = {total_score_part_one}")
    logging.info(f"total score part two = {total_score_part_two}")

        
        