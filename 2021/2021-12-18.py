from __future__ import annotations
from typing import Any

class SFN:
    def __init__(self, input: list[Any], up: None|SFN = None, is_right: bool = False) -> None:
        self.left: int | SFN
        self.right: int | SFN
        self.up = up
        self.is_right = is_right
        left, right = input[0], input[1]
        if type(left) == int:
            self.left = left
        elif type(left) == list:
            self.left = SFN(left, self, False)
        if type(right) == int:
            self.right = right
        elif type(right) == list:
            self.right = SFN(right, self, True)
    
    def __repr__(self) -> str:
        return f'SFN({self.AsList()})'

    def AsList(self) -> list[Any]:
        left: int | list[Any] = self.left if type(self.left) == int else self.left.AsList()
        right: int | list[Any] = self.right if type(self.right) == int else self.right.AsList()
        return [left, right]

    def __add__(self, other: SFN) -> SFN:
        r = SFN([self.AsList(), other.AsList()])
        while True:
            if r.Explode():
                continue
            if r.Split():
                continue
            break
        return r


    def Reduce(self):
        self.Explode()
        self.Split()

    def Explode(self) -> bool:
        # If any pair is nested inside four pairs, the leftmost such pair
        # explodes.
        sfn_node: SFN | None = self.FindNode(depth=4)
        if sfn_node is None: return False
        assert type(sfn_node.left) == int
        assert type(sfn_node.right) == int
        # To explode a pair, the pair's left value is added to the first regular
        # number to the left of the exploding pair (if any), and the pair's right 
        # value is added to the first regular number to the right of the exploding 
        # pair (if any). Exploding pairs will always consist of two regular numbers. 
        sfn_node.AddToNextLeft(sfn_node.left)
        sfn_node.AddToNextRight(sfn_node.right)
        # Then, the entire exploding pair is replaced with the regular number 0.
        if sfn_node.is_right:
            sfn_node.up.right = 0
        else:
            sfn_node.up.left = 0
        return True
    
    def FindNode(self, depth:int) -> SFN | None:
        if depth == 0:
            return self
        result: SFN | None = None
        if type(self.left) == SFN:
            result = self.left.FindNode(depth-1)
            if result:
                return result
        if type(self.right) == SFN:
            result = self.right.FindNode(depth-1)
        return result

    def AddToNextLeft(self, value: int):
        # We're not on the right, so we need to go up to look for a left.
        if not self.is_right:
            if self.up:
                self.up.AddToNextLeft(value)
        
        # We're on the right, so there must be _something_ left of us.
        elif self.is_right and self.up:
            if type(self.up.left) == int:
                self.up.left += value
            elif type(self.up.left) == SFN:
                landing_zone = self.up.left
                while type(landing_zone.right) != int:
                    landing_zone = landing_zone.right
                assert type(landing_zone.right) == int
                landing_zone.right += value

    def AddToNextRight(self, value: int):
        # We're not on the left, so we need to go up to look for a right.
        if self.is_right:
            if self.up:
                self.up.AddToNextRight(value)
        
        # We're on the left, so there must be _something_ right of us.
        elif not self.is_right and self.up:
            if type(self.up.right) == int:
                self.up.right += value
            elif type(self.up.right) == SFN:
                landing_zone = self.up.right
                while type(landing_zone.left) != int:
                    landing_zone = landing_zone.left
                assert type(landing_zone.left) == int
                landing_zone.left += value

    def Split(self) -> bool:
        # If any regular number is 10 or greater, the leftmost such regular 
        # number splits.
        if type(self.left) == int and self.left >= 10:
            self.left = SFN([self.left // 2, (self.left+1) // 2], self, False)
            return True
        elif type(self.left) == SFN:
            result = self.left.Split()
            if result: return result
        if type(self.right) == int and self.right >= 10:
            self.right = SFN([self.right // 2, (self.right+1) // 2], self, True)
            return True
        elif type(self.right) == SFN:
            return self.right.Split()
        return False
    
    def Magnitude(self) -> int:
        magnitude:int = 0
        if type(self.left) == int:
            magnitude += 3 * self.left
        else:
            magnitude += 3 * self.left.Magnitude()
        if type(self.right) == int:
            magnitude += 2 * self.right
        else:
            magnitude += 2 * self.right.Magnitude()
        return magnitude

SAMPLE_TEST = [
    # Just explodes
    ([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]],
     [[[[0,7],4],[[7,8],[6,0]]],[8,1]]),
    ([[[[[9,8],1],2],3],4], [[[[0,9],2],3],4]),
    ([7,[6,[5,[4,[3,2]]]]], [7,[6,[5,[7,0]]]]),
    ([[6,[5,[4,[3,2]]]],1], [[6,[5,[7,0]]],3]),
    ([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
     [[3,[2,[8,0]]],[9,[5,[7,0]]]]),
    # Explodes and splits
    ([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]],
     [[[[0,7],4],[[7,8],[6,0]]],[8,1]]),
]

for input, output in SAMPLE_TEST:
    s = SFN(input)
    # print(f'STRT: {s}')
    while True:
        if s.Explode():
            # print(f'EXPL: {s}')
            continue
        if s.Split():
            # print(f'SPLT: {s}')
            continue
        break
        
    try:
        assert f'{s}' == f'SFN({output})'
    except AssertionError:
        print(f'FAIL: {s} != {output}')
        s = SFN(input)
        print(f'FindNode@4: {s.FindNode(depth=4)}')

with open('2021-12-18.txt') as f:
    s = None
    for line in f:
        line = eval(line.strip())
        if not s:
            s = SFN(line)
            continue
        s += SFN(line)

print(f'{s}')
print(f'{s.Magnitude()}')

lines: list[Any] = []
with open('2021-12-18.txt') as f:
    for line in f:
        lines.append(eval(line.strip()))

max_mag = 0
for i in range(len(lines)):
    for j in range(len(lines)):
        if i != j:
            max_mag = max(max_mag,(SFN(lines[i]) + SFN(lines[j])).Magnitude())

print(f'{max_mag}')
