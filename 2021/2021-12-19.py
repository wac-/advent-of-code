from __future__ import annotations
from collections import defaultdict
import itertools
from typing import Any, Iterable


class Coordinate(object):
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x, self.y, self.z = x, y, z

    def __repr__(self) -> str:
        return f'<{self.x}, {self.y}, {self.z}>'

    def __hash__(self) -> int:
        return tuple([self.x, self.y, self.z]).__hash__()

    def __sub__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x-other.x, self.y-other.y, self.z-other.z)

    def __add__(self, other: Coordinate) -> Coordinate:
        return Coordinate(self.x+other.x, self.y+other.y, self.z+other.z)

    def __mul__(self, transform: tuple[int, ...]) -> Coordinate:
        return Coordinate(self.x * transform[0], self.y * transform[1], self.z * transform[2])

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Coordinate) and (self.x == __o.x and
                                                self.y == __o.y and self.z == __o.z)

    def __lt__(self, other: Coordinate) -> bool:
        if self.x == other.x:
            if self.y == other.y:
                return self.z < other.z
            return self.y < other.y
        return self.x < other.x

    def Reorder(self, ordering: tuple[int, ...]) -> Coordinate:
        assert set(ordering) == set([0, 1, 2])
        coord_tuple = (self.x, self.y, self.z)
        return Coordinate(*(coord_tuple[ordering[i]] for i in (0, 1, 2)))

    def IsTransformation(self, other: Coordinate) -> bool:
        for ordering in itertools.permutations((0, 1, 2), 3):
            for transform in itertools.product((-1, 1), repeat=3):
                if self == other.Reorder(ordering) * transform:
                    return True
        return False

    def Normalize(self) -> Coordinate:
        return Coordinate(*(sorted([abs(self.x), abs(self.y), abs(self.z)])))


class Scanner(list[Coordinate]):
    def __init_subclass__(cls) -> None:
        return super().__init_subclass__()

    def PopulateProbeDistances(self):
        self.probe_distances: dict[tuple[int, int], Coordinate] = {}
        for a, b in itertools.combinations(range(len(self)), 2):
            self.probe_distances[(a, b)] = self.ProbeDistance(a, b)

    def ProbeDistance(self, a: int, b: int) -> Coordinate:
        return self[a] - self[b]

    def ProbeDistances(self) -> Iterable[tuple[int, int, Coordinate]]:
        for a, b in itertools.combinations(range(len(self)), 2):
            yield (a, b, self.ProbeDistance(a, b))

    def NormalizedProbeDistances(self) -> Iterable[tuple[int, int, Coordinate]]:
        for a, b, distance in self.ProbeDistances():
            yield (a, b, distance.Normalize())


assert Coordinate(1, 2, 3).IsTransformation(Coordinate(-3, 1, -2))


def ScannersFromFile(filename: str) -> dict[int, Scanner]:
    scanners: dict[int, Scanner] = {}
    with open(filename) as f:
        scanner = 0
        for line in (l.strip() for l in f):
            if not line:
                continue
            if line.startswith('--- scanner '):
                scanner = int(line.removeprefix(
                    '--- scanner ').removesuffix(' ---'))
                scanners[scanner] = Scanner()
                continue
            c = Coordinate(*(int(n) for n in line.split(',')))
            scanners[scanner].append(c)
    return scanners


sample_scanners = ScannersFromFile('2021-12-19.sample.txt')
day_scanners = ScannersFromFile('2021-12-19.txt')


def CountUnique(iterable: Iterable[Any]) -> int:
    "Count unique elements."
    seen: set[Any] = set()
    for element in itertools.filterfalse(seen.__contains__, iterable):
        seen.add(element)
    return len(seen)

# Find commons.
# Build list of scanner N, probe N_a, probe N_b, scanner_M, probe M_a, probe M_b


def ProbeDistanceProbesList(scanners: dict[int, Scanner]) -> dict[Coordinate, list[tuple[int, int, int]]]:
    probe_dist_matches: dict[Coordinate,
                             list[tuple[int, int, int]]] = defaultdict(list)

    for n, scanner in scanners.items():
        for a, b, norm_dist in scanner.NormalizedProbeDistances():
            probe_dist_matches[norm_dist].append((n, a, b))
    return probe_dist_matches

# Luckily the same probe distance doesn't appear twice in the same scanner.
probe_dist_matches = ProbeDistanceProbesList(sample_scanners)

print(f'{len(probe_dist_matches)}')
for norm_dist, dist_matches in probe_dist_matches.items():
    if len(dist_matches) > 1:
        print(f'{norm_dist} : {dist_matches}')

# Now we want a list of [scanner, probe] -> [[scanner, probe], [scanner,probe]] possibilities

mapping: dict[tuple[int,int], set[tuple[int,int]]] = {}

for dist_matches in probe_dist_matches.values():
    if len(dist_matches) > 1:
        probes: list[tuple[int, int]] = []
        # [(a, b, c), (d, e, f), (g, h, i)] -->
        #  (a,b) -> [(d,e), (d,f), (g,h), (g,i)]
        #  (a,c) -> [(d,e), (d,f), (g,h), (g,i)]
        for x in dist_matches:
            probes += [(x[0], x[1]), (x[0], x[2])]
        for (sensor_a, probe_a) in probes:
            other_probe_set: set[tuple[int, int]] = set(probes)
            other_probe_set.remove((sensor_a, probe_a))
            if (sensor_a, probe_a) in mapping:
                mapping[(sensor_a, probe_a)].intersection_update(other_probe_set)
            else:
                mapping[(sensor_a, probe_a)] = other_probe_set

print(f'{mapping}')
for k, v in mapping:
    if mapping[v[0]]
                
