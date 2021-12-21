from queue import PriorityQueue

Coordinate = tuple[int, int]

map: list[list[int]] = []

PART_TWO = True

# For each position, we store the lowest cost path to get there.
lowest_cost: list[list[None | tuple[int, list[Coordinate]]]] = []

with open('2021-12-15.txt') as f:
    for line in (l.strip() for l in f):
        map_values = [int(x) for x in line]
        if PART_TWO:
            for i in range(1,5):
                map_values += [(int(x)+i) for x in line]
        map.append(map_values)
        lowest_cost.append([None] * len(map_values))

if PART_TWO:
    # Expand map 4 times below.
    orig_map_len = len(map)
    for i in range(1,5):
        for y in range(orig_map_len):
            map.append([(x+i) for x in map[y]])
            lowest_cost.append([None] * len(map[0]))

    # Deal with overflows: At most 9+4, so just subtract 9 as needed.
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] > 9:
                map[y][x] -= 9

# Priority queue always draws the current lowest cost path
work_queue: PriorityQueue[tuple[int,Coordinate, list[Coordinate]]] = PriorityQueue()

work_queue.put_nowait((0,(0,0),[(0,0)]))

NEIGHBORS = ((-1, 0), (1, 0), (0, 1), (0, -1))

max_y, max_x = len(map)-1, len(map[0])-1

while not work_queue.empty():
    cost, (x, y), path = work_queue.get_nowait()
    if lowest_cost[max_y][max_x] is not None:
        if lowest_cost[max_y][max_x][0] < cost:
            # Drain task if there is already a cheaper way to reach the end.
            work_queue.task_done()
            break
    if lowest_cost[y][x] is not None and lowest_cost[y][x][0] < cost:
        work_queue.task_done()
        continue
    lowest_cost[y][x] = (cost, path)
    for dx, dy in NEIGHBORS:
        nx, ny = x+dx, y+dy
        # Skip out of bounds
        if min(nx, ny) < 0 or ny > max_y or nx > max_x:
            continue
        new_cost = cost + map[ny][nx]
        new_path = path + [(nx, ny)]
        # Skip unless we're getting there cheaper.
        if lowest_cost[ny][nx] is not None:
            if lowest_cost[ny][nx][0] <= new_cost:
                continue
        # NOT THREAD SAFE:
        lowest_cost[ny][nx] = (new_cost, new_path)
        work_queue.put_nowait((new_cost, (nx, ny), new_path))
    work_queue.task_done()

print(lowest_cost[max_y][max_x])

print(lowest_cost[max_y][max_x][0])

