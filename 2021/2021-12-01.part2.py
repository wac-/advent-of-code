with open("2021-12-01.txt") as input_file:
    increasing_lines = 0
    last_ints = [None, None, None]
    for input_line in input_file:
        if (None not in last_ints):
            last_ints_sum = sum(last_ints)
        else:
            last_ints_sum = None
        input_int = int(input_line)
        _ = last_ints.pop()
        last_ints.insert(0, input_int)

        if (last_ints_sum is not None) and sum(last_ints) > last_ints_sum:
            increasing_lines += 1
    print(increasing_lines)
