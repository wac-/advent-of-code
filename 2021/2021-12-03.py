
with open('2021-12-03.txt') as f:
    bit_counts = None
    row_count = 0

    for line in f:
        if bit_counts is None:
            bit_counts = [0] * len(line.strip())
        line = [int(i) for i in line.strip()]
        for i in range(len(bit_counts)):
            bit_counts[i] += line[i]
        row_count += 1
    
    print(bit_counts)

    most_common_bits = [1 if i > (row_count/2) else 0 for i in bit_counts]
    gamma_binary = (''.join(map(str, most_common_bits)))
    gamma_int = int(gamma_binary, 2)
    epsilon_int = gamma_int ^ int("1" * len(bit_counts), 2)
    print(''.join(str(x) for x in line))
    print(gamma_binary)
    print(gamma_int)
    print(epsilon_int)
    print(gamma_int * epsilon_int)