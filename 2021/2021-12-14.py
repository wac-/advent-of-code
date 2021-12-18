from collections import Counter

initial: str = ''
next_work: dict[str, tuple[str,str]] = {}

with open('2021-12-14.txt') as f:
    for line in (l.strip() for l in f):
        if '->' in line:
            pair, insert = (x.strip() for x in line.split('->'))
            next_work[pair] = (pair[0] + insert, insert + pair[1])
        elif line:
            initial = line

MAX_ITERATION = 40

initial_pair_count: Counter[str] = Counter()

for c in range(len(initial)-1):
    initial_pair_count[initial[c:c+2]] += 1

pair_count = initial_pair_count

for i in range(MAX_ITERATION):
    next_pair_count: Counter[str] = Counter()
    for key in pair_count:
        new_pairs = next_work[key]
        for new_pair in new_pairs:
            next_pair_count[new_pair] += pair_count[key]
    pair_count = next_pair_count

element_count: Counter[str] = Counter()
for pair, count in pair_count.items():
    element_count[pair[0]] += count

# Add the last element that would otherwise get skipped.
element_count[initial[-1]] += 1

print(f'{element_count.total()} = '
      f'{max(element_count.values()) - min(element_count.values())}')
