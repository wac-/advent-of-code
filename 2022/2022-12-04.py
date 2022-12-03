#!/usr/bin/env python3
import logging

logging.getLogger().setLevel(logging.INFO)

def ParseInput(input: str) -> tuple[set[int]]:
    cleaning_assignments: list[str] = input.split(',')
    cleaning_sets: list[set[int]] = []
    for cleaning_assignment in cleaning_assignments:
        bottom, top = map(int, cleaning_assignment.split('-'))
        cleaning_sets.append(set(range(bottom, top+1)))
    return tuple(cleaning_sets)

def AssignmentsAreSubset(assignments: tuple[set[int]]) -> bool:
    assert len(assignments) == 2
    first: set[int] = assignments[0]
    second: set[int] = assignments[1]
    return first.issubset(second) or second.issubset(first)

def AssignmentsOverlap(assignments: tuple[set[int]]) -> bool:
    assert len(assignments) == 2
    first: set[int] = assignments[0]
    second: set[int] = assignments[1]
    return len(first.intersection(second)) > 0

subset_assignment_count: int = 0
overlap_assignment_count: int = 0

with open('2022/2022-12-04.txt') as input_file:
    for input_line in input_file:
        assignment_part: tuple[set[int]] = ParseInput(input_line.strip())
        if AssignmentsAreSubset(assignment_part):
            subset_assignment_count += 1
        if AssignmentsOverlap(assignment_part):
            overlap_assignment_count += 1

logging.info(f'subset assignment count = {subset_assignment_count}')
logging.info(f'overlapping assignment count = {overlap_assignment_count}')
