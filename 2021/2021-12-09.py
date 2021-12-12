import functools

map: list[list[int]] = []

with open('2021-12-09.txt') as f:
    for line in f:
        map.append([int(n) for n in line.strip()])

risk_level_sum = 0

minima_coords: list[tuple[int, int]] = []

for y in range(len(map)):
    for x in range(len(map[y])):
        this_cell: int = map[y][x]
        neighbors: list[int] = []
        for (dy,dx) in ((-1,0),(1,0),(0,-1),(0,1)):
            try:
                assert(y+dy >= 0 and x+dx >= 0)
                neighbors.append(map[y+dy][x+dx])
            except:
                pass
        if this_cell < min(neighbors):
            # Low point.
            minima_coords.append((x,y))
            risk_level_sum += this_cell + 1

visited_map: list[list[bool]] = [[False for _ in x] for x in map]

# Sizes so far.
sizes: list[int] = []

# Next to visit in current search.
stack: list[tuple[int,int]] = []

for y in range(len(map)):
    for x in range(len(map[y])):
        # Skip starting a search here if we're already here.
        if visited_map[y][x]:
            continue
        size = 0
        stack = [(x,y)]
        while stack:
            cx,cy = stack.pop()
            if visited_map[cy][cx]: continue
            visited_map[cy][cx] = True
            if map[cy][cx] == 9:
                continue
            size += 1
            for (dy,dx) in ((-1,0),(1,0),(0,-1),(0,1)):
                if min(cx+dx, cy+dy) < 0: continue
                if cy+dy >= len(map):
                    continue
                if cx+dx >= len(map[y]):
                    continue
                assert cx+dx < 100
                assert cy+dy < 100
                stack.append((cx+dx, cy+dy))

        # Reached the end of stack
        sizes.append(size)

print(sizes)

#for y in range(len(map)):
#    for x in range(len(map[y])):
#        print('{}{}'.format(map[y][x], '*' if (x,y) in minima_coords else ' '), end='')
#    print('')

print('Part 1: {}'.format(risk_level_sum))
print('Part 2: {}'.format(functools.reduce(lambda a,b: a*b, sorted(sizes)[-3:])))