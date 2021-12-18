from typing import Iterable, NamedTuple

class Coordinate(NamedTuple):
    x: int
    y: int

class Fold(NamedTuple):
    axis: str
    line: int

base_dots: list[Coordinate] = []
folds: list[Fold] = []

with open('2021-12-13.txt') as f:
    for line in f:
        if ',' in line:
            x, y = line.strip().split(',')
            base_dots.append(Coordinate(int(x),int(y)))
        if line.startswith('fold along '):
            axis, line = line[11:].strip().split('=')
            folds.append(Fold(axis, int(line)))


def RenderSheet(dots: Iterable[Coordinate]) -> None:
    max_x, max_y = max(d.x for d in dots), max(d.y for d in dots)
    for cur_y in range(max_y+1):
        text_line: str = ''
        for cur_x in range(max_x+1):
            if Coordinate(cur_x, cur_y) in dots:
                text_line += '#'
            else:
                text_line += '.'
        print(text_line)

# 7 -> 0 1 2 3 4 5 6 7 6 5 4 3 2 1 0
#                      8 9 1011121314
# min(abs(n),abs(2*k - n))
def FoldSheet(dots: Iterable[Coordinate], axis: str, line: int) -> set[Coordinate]:
    folded_list: set[Coordinate] = set()
    for dot in dots:
        x,y = dot.x, dot.y
        if axis == 'x':
            # Skip negative coordinate outcomes.
            if x > 2*line:
                continue
            x = min(abs(x), abs(2*line - x))
        if axis == 'y':
            # Skip negative coordinate outcomes.
            if y > 2*line:
                continue
            y = min(abs(y), abs(2*line - y))
        folded_list.add(Coordinate(x,y))
    return folded_list

# RenderSheet(base_dots)
# print()
dots: set[Coordinate] = set(base_dots)
for axis, line in folds:
    dots = FoldSheet(dots, axis, line)
    print(f'Folding {axis}={line} gives {len(dots)} dots.')
    # RenderSheet(dots)
    # print()

RenderSheet(dots)
