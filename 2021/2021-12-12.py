from collections import defaultdict

vectors: defaultdict[str, list[str]] = defaultdict(lambda: list())
complete_paths: list[list[str]] = []

with open('2021-12-12.txt') as f:
    for line in f:
        src, dst = line.strip().split('-')
        vectors[src].append(dst)
        vectors[dst].append(src)

# current node, revisited small room, path so far
# if dst is lower, look for it in path and reject.
stack: list[tuple[str, str|None, list[str]]] = []

# We start at start...
stack.append(('start', None, ['start']))

while stack:
    src, revisit, path = stack.pop()
    if src == 'end':
        if path not in complete_paths:
            complete_paths.append(path)
        continue
    dsts = vectors[src]
    for dst in dsts:
        if dst.islower() and dst in path:
            if revisit is None and dst != 'start':
                stack.append((dst, dst, path+[dst]))
            continue
        stack.append((dst, revisit, path+[dst]))

#output_txt = []
#for path in complete_paths:
#    output_txt.append(','.join(path))
#for path in sorted(output_txt):
#    print(path)

print(len(complete_paths))