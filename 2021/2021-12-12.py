from collections import defaultdict
from typing import Any

vectors: defaultdict[str, list[str]] = defaultdict(lambda: list())
complete_paths: list[list[str]] = []

with open('2021-12-12.txt') as f:
    for line in f:
        src, dst = line.strip().split('-')
        vectors[src].append(dst)
        vectors[dst].append(src)

def NewVisitedDict(paths: dict[str, Any]) -> dict[str, bool]:
    visited_dict: dict[str, bool] = dict()
    for room in paths:
        if room.islower():
            visited_dict[room] = False
    return visited_dict

# current node, path so far
# if dst is lower, look for it in path and reject.
stack: list[tuple[str, list[str]]] = []

# We start at start...
stack.append(('start',['start']))

while stack:
    src, path = stack.pop()
    if src == 'end':
        if path not in complete_paths:
            complete_paths.append(path)
        continue
    dsts = vectors[src]
    for dst in dsts:
        if dst.islower() and dst in path:
            continue
        stack.append((dst, path+[dst]))

#output_txt = []
#for path in complete_paths:
#    output_txt.append(','.join(path))
#for path in sorted(output_txt):
#    print(path)

print(len(complete_paths))