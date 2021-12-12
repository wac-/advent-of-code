REPORT_STEPS = 100
MAX_STEPS = 1000
SANITY_CHECKS = True
NEIGHBORS = ((-1,1), (0,1), (1,1), (-1,0), (1,0), (-1,-1), (0,-1), (1,-1))

octo_array: list[list[int]] = []

step = -1
all_flash_step = None
total_flash_count = 0

with open('2021-12-11.txt') as f:
    for line in f:
        octo_array.append([int(c) for c in line.strip()])

if SANITY_CHECKS:
    # The input is a square with no shenanigans.
    assert 1 == len(set(len(x) for x in octo_array))
    assert len(octo_array) == len(octo_array[0])

for step in range(MAX_STEPS):
    pass
    # Increment energy levels everywhere in the array
    flash_stack: list[tuple[int,int]] = []

    for row in range(len(octo_array)):
        for col in range(len(octo_array[row])):
            octo_array[row][col] += 1
            if octo_array[row][col] > 9:
                flash_stack.append((row,col))

    # Do flashes
    flashed: list[list[bool]] = [
        [False for _ in row] for row in octo_array
    ]

    if SANITY_CHECKS: assert len(flashed) == len(flashed[0]) == len(octo_array)
    while flash_stack:
        row, col = flash_stack.pop()
        # Already flashed? Skip to next.
        if flashed[row][col]:
            continue
        flashed[row][col] = True
        # Increment neighbors.
        for nrow, ncol in NEIGHBORS:
            # Keep us inbounds.
            if min(row+nrow, col+ncol) < 0: continue
            if max(row+nrow, col+ncol) >= len(octo_array): continue
            octo_array[row+nrow][col+ncol] += 1
            if octo_array[row+nrow][col+ncol] > 9:
                flash_stack.append((row+nrow,col+ncol))

    # Set flashed to energy to zero
    flash_count = 0
    for row in range(len(octo_array)):
        for col in range(len(octo_array[row])):
            if flashed[row][col]:
                octo_array[row][col] = 0
                flash_count += 1

    # Part 2: Record first step where all flash.
    if not all_flash_step and flash_count == len(octo_array) * len(octo_array[0]):
        all_flash_step = step+1
    total_flash_count += flash_count
    if step+1 == REPORT_STEPS:
        print('step {} total flash count: {}'.format(step+1, total_flash_count))
    if step+1 > REPORT_STEPS and all_flash_step:
        break

print('all flash step {}'.format(all_flash_step))