#!/usr/bin/env python3
import logging

logging.getLogger().setLevel(logging.INFO)

elf_calories: list[int] = []

with open('2022/2022-12-01.part1.txt') as input_file:
    last_line_empty: bool = True
    for input_line in input_file:
        # Remove extraneous nonsense.
        input_line: str = input_line.strip()
        if not input_line:
            last_line_empty = True
            continue
        input_int: int = int(input_line)
        if last_line_empty:
            elf_calories.append(0)
        elf_calories[-1] += input_int
        last_line_empty = False

logging.debug(elf_calories)


def IndexOfMax(a_list: list[int]) -> int:
    assert len(a_list)
    cur_max: int = a_list[0]
    max_index: int = 0
    for i in range(len(a_list)):
        if a_list[i] > cur_max:
            cur_max = a_list[i]
            max_index = i
    return max_index


max_index: int = IndexOfMax(elf_calories)
logging.info("max index: {} ({})".format(max_index+1,
                                         elf_calories[max_index]))

logging.info("top three: {}".format(sorted(elf_calories)[-3:]))

logging.info("sum top three: {}".format(sum(sorted(elf_calories)[-3:])))