
with open('2021-12-02.txt') as input_file:
    horiz_pos: int = 0
    vert_pos: int = 0
    aim: int = 0
    for line in input_file:
        direction: str, count: str = line.split(" ")
        count: int = int(count)
        if direction == 'forward':
            horiz_pos += count
            vert_pos = max(0, vert_pos + (aim * count))
        elif direction == 'down':
            # vert_pos += count
            aim += count
        elif direction == 'up':
            # vert_pos = max(0, vert_pos - count)
            aim -= count
    
        print('h: {} v: {} aim:{}'.format(horiz_pos, vert_pos, aim))
        print('puzz: ', horiz_pos*vert_pos)