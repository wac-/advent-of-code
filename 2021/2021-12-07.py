from collections import defaultdict

part_one: bool = False

# key is position of crab, value is count of crabs at position.
crab_count: defaultdict[int, int] = defaultdict(lambda: 0)

with open('2021-12-07.txt') as f:
    crab_pos_text = f.readline().strip()
    for crab in crab_pos_text.split(','):
        crab_count[int(crab)] += 1

max_crab: int = max(crab_count.keys())
min_crab: int = min(crab_count.keys())

# key is position of exit, value is total fuel spent.
fuel_per_distance: defaultdict[int, int] = defaultdict(lambda: 0)
for pos in range(min_crab, max_crab+1):
    for crab_pos in crab_count:
        distance: int = abs(pos - crab_pos)
        if part_one:
            fuel_spend_per_crab: int = distance
        else:
            # fuel spend is sigma(n)
            fuel_spend_per_crab: int = (distance * (distance + 1)) // 2
        fuel_per_distance[pos] += fuel_spend_per_crab * crab_count[crab_pos]

print("min: {}".format(min(fuel_per_distance.values())))
print("max: {}".format(max(fuel_per_distance.values())))