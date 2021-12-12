from collections import defaultdict

coordinate = tuple[int,int]

max_x = 0
max_y = 0

consider_diagonals = True

coords_list: list[tuple[tuple[int,...],...]] = []
with open('2021-12-05.txt') as f:
    for line in f:
        coords_text: list[str] = line.split(' -> ', 2)
        # Force them into sorted order, because it's super helpful.
        coords = tuple(sorted(
            tuple(int(n) for n in coord_text.split(',',2))
            for coord_text in coords_text))
        coords_list.insert(-1, coords)

danger_spots: dict[tuple[int,int], int] = defaultdict(lambda: 0)
for coords in coords_list:
    x_1, y_1 = coords[0]
    x_2, y_2 = coords[1]

    # Move max trackers
    max_x = max(max_x, x_1, x_2)
    max_y = max(max_y, y_1, y_2)

    # Draw vert line, if x coord matches.
    if x_1 == x_2:
        x_coord = x_1
        for y_coord in range(y_1, y_2+1):
            danger_spots[(x_coord, y_coord)] += 1
    elif y_1 == y_2:
        y_coord = y_1
        for x_coord in range(x_1, x_2+1):
            danger_spots[(x_coord, y_coord)] += 1
    elif consider_diagonals:
        # Remaining lines must be diagonal.
        assert(abs(x_1-x_2) == abs(y_1-y_2))

        x_coord, y_coord = x_1, y_1
        x_step = 1 if x_2 > x_1 else -1
        y_step = 1 if y_2 > y_1 else -1
        danger_spots[(x_coord, y_coord)] += 1
        while (x_coord, y_coord) != (x_2, y_2):
            x_coord += x_step
            y_coord += y_step
            danger_spots[(x_coord, y_coord)] += 1


#print("Danger Map:")
#for y_coord in range(max_y+1):
#    for x_coord in range(max_x+1):
#        danger_level = danger_spots[(x_coord, y_coord)]
#        print("{}".format(danger_level if danger_level else '.'), end='')
#    print()

for x in range(1, max(danger_spots.values())+1):
    print('danger level == {}: {}'.format(x, 
        len([n for n in danger_spots.values() if n == x])))
    print('danger level >= {}: {}'.format(x, 
        len([n for n in danger_spots.values() if n >= x])))
