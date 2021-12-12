with open("2021-12-01.txt") as input_file:
    increasing_lines = 0
    last_int = None
    for input_line in input_file:
        input_int = int(input_line)
        if (last_int is not None) and input_int > last_int:
            increasing_lines += 1
        last_int = input_int
    print(increasing_lines)
