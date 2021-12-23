from typing import NamedTuple

SAMPLE_INPUT = 'target area: x=20..30, y=-10..-5'
INPUT = 'target area: x=138..184, y=-125..-71'

Coordinate = NamedTuple('Coordinate', [('x', int),('y', int)])
Box = tuple[Coordinate, Coordinate]

def ParseInputToBoxCorners(input: str) -> Box:
    input = input.strip()
    assert input.startswith('target area: ')
    input = input.removeprefix('target area: ')
    x_range_str, y_range_str = (s.strip() for s in input.split(','))
    assert x_range_str.startswith('x=')
    assert y_range_str.startswith('y=')
    x_range_str, y_range_str = x_range_str.removeprefix('x='), y_range_str.removeprefix('y=')
    # Strings are now '_n_.._m_'
    x_range = tuple(int(n) for n in x_range_str.split('..'))
    y_range = tuple(int(n) for n in y_range_str.split('..'))
    # Order doesn't matter. It's a box.
    return (Coordinate(x_range[0],y_range[0]), Coordinate(x_range[1],y_range[1]))

def PointWithinBox(point: Coordinate, box: Box) -> bool:
    return (point.x in range(box[0].x, box[1].x+1) and
            point.y in range(box[0].y, box[1].y+1))

def PointBeyondBox(point: Coordinate, box: Box) -> bool:
    return point.x > box[1].x or point.y < box[0].y

class MissShot(Exception):
    pass
class ShortShot(MissShot):
    pass
class LongShot(MissShot):
    pass

def TryShot(vector: Coordinate, box: Box) -> int:
    max_y = 0
    probe = Coordinate(0,0)
    while not PointBeyondBox(probe, box):
        probe = Coordinate(probe.x + vector.x, probe.y + vector.y)
        dx_adjustment = 0 if vector.x == 0 else vector.x // abs(vector.x)
        vector = Coordinate(vector.x - dx_adjustment, vector.y - 1)
        max_y = max(max_y, probe.y)
        if PointWithinBox(probe, box):
            return max_y
    # __L
    # _TM
    # SMM
    if probe.x < box[0].x and probe.y < box[0].y:
        raise ShortShot
    if probe.x > box[1].x and probe.y > box[1].y:
        raise LongShot
    raise MissShot

def FindHighestShot(input: str) -> tuple[int,int]:
    result = 0
    hits: set[Coordinate] = set()
    box = ParseInputToBoxCorners(input)
    # Narrow reasonable X vectors.
    min_x_vec: int = box[1].x+1
    for dx in range(box[1].x+1):
        x_pos = 0
        x_vec = dx
        while x_vec != 0:
            x_pos += x_vec
            x_vec -= x_vec // abs(x_vec)
        if x_pos in range(box[0].x, box[1].x):
            min_x_vec = min(dx, min_x_vec)
        if x_pos > box[1].x: 
            break
    print(f'Reasonable x: {min_x_vec}..')

    for dx in range(min_x_vec, box[1].x+1):
        dy = box[0].y
        misses = 0
        while True:
            try:
                result = max(result, TryShot(Coordinate(dx,dy), box))
                hits.add(Coordinate(dx,dy))
                # print(f'HIT: {dx:4d}, {dy:4d}')
                dy += 1
            except LongShot:
                # print(f'LONG:{dx:4d}, {dy:4d}')
                break
            except ShortShot:
                # print(f'SHRT:{dx:4d}, {dy:4d}')
                dy += 1
            except MissShot:
                # print(f'MISS:{dx:4d}, {dy:4d}')
                dy += 1
                misses += 1
                if misses > 63:  # This magic number feels very bad.
                    break
    return result, len(hits)

print(FindHighestShot(SAMPLE_INPUT))
print()
print(FindHighestShot(INPUT))
