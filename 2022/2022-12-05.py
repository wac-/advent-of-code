#!/usr/bin/env python3
from collections import defaultdict
from copy import deepcopy
import logging
from typing import Iterable

logging.getLogger().setLevel(logging.INFO)

ElvenStack = dict[int, list[str]]

def ParseStacks(text: Iterable[str]) -> ElvenStack:
    stacks: ElvenStack = defaultdict(list)
    stack_mapping: dict[int, int] = {}
    for line in text:
        line = line.rstrip()

        # Is this the line break?
        if len(line) == 0:
            break
        position = 0
        while position < len(line):
            # Start of a container.
            if line[position] == '[':
                stack: list[str] = stacks[position // 4]
                stack.insert(0, line[position+1])
            elif line[position+1].isdigit():
                stack_mapping[position // 4] = int(line[position+1])
            position += 4

    # Protect ourselves against the stack numbers doing something weird.
    remapped_stacks: ElvenStack = {}
    for stack_number in stack_mapping:
        elven_stack_number: int = stack_mapping[stack_number]
        remapped_stacks[elven_stack_number] = stacks[stack_number]

    return remapped_stacks

class StackMoveInstruction(object):
    def __init__(self, move_from: int, move_to: int, count: int) -> None:
        self.move_from = move_from
        self.move_to = move_to
        self.count = count

    def __repr__(self) -> str:
        return f"<StackMoveInstruction move {self.count} from {self.move_from} to {self.move_to}>"

    def DoMove(self, orig_stacks: ElvenStack, part: int = 2) -> ElvenStack:
        # Avoid side-effecting the stack by making a working copy.
        stacks: ElvenStack = deepcopy(orig_stacks)
        if part == 1:
            for _ in range(self.count):
                stacks[self.move_to].append(
                    stacks[self.move_from].pop())
            return stacks
        elif part == 2:
            inter_stack: list[str] = []
            for _ in range(self.count):
                inter_stack.append(
                    stacks[self.move_from].pop())
            for _ in range(self.count):
                stacks[self.move_to].append(
                    inter_stack.pop())
            return stacks
        else:
            raise NotImplementedError()
        

def ParseInstructions(text: Iterable[str]) -> list[StackMoveInstruction]:
    instructions: list[StackMoveInstruction] = []
    for line in text:
        line = line.strip().split()
        instructions.append(
            StackMoveInstruction(count = int(line[1]),
                                 move_from=int(line[3]),
                                 move_to=int(line[5]))
        )
    return instructions

def FormatStacks(stacks: ElvenStack) -> str:
    output: str = ''
    tallest_stack_len: int = max(map(len, stacks.values()))
    ordered_stack_labels: list[int] = sorted(stacks.keys())
    for i in range(tallest_stack_len-1, -1, -1):
        for stack_label in ordered_stack_labels:
            try:
                output += f'[{stacks[stack_label][i]}] '
            except IndexError:
                output += '    '
        output += '\n'
    for stack_label in ordered_stack_labels:
        output += f' {stack_label}  '
    output += '\n'
    return output

def TopOfStacks(stacks: ElvenStack) -> str:
    output: str = ''
    ordered_stack_labels: list[int] = sorted(stacks.keys())
    for stack_label in ordered_stack_labels:
        output += stacks[stack_label][-1]
    return output


with open('2022/2022-12-05.txt') as input_file:
    stacks = ParseStacks(input_file)
    logging.info('\n'+FormatStacks(stacks))
    instructions = ParseInstructions(input_file)
    for instruction in instructions:
        stacks = instruction.DoMove(stacks)
    
    logging.info('\n'+FormatStacks(stacks))
    print(TopOfStacks(stacks))
