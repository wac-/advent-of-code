
with open('2021-12-03.txt') as f:
    sorted_lines = sorted(line.strip() for line in f)

num_digits = len(sorted_lines[0])

top_index = 0
bottom_index = len(sorted_lines)
for bit in range(num_digits):
    # print("b {}: [{}:{}]".format(bit, top_index, bottom_index))
    # Find the split point
    for i in range(top_index, bottom_index):
        # Looking for the first bit set to 1.
        if sorted_lines[i][bit] == '1':
            # Are we closer to the top?
            distance_to_top = i - top_index
            distance_to_bottom = bottom_index - i
            if distance_to_top <= distance_to_bottom:
                # Then 1s are more prevelant, reset top to here
                # and run the loop on the next bit.
                top_index = i
                break
            else:
                # Then 0s are more prevelant reset bottom to here
                bottom_index = i
                break
    if len(sorted_lines[top_index:bottom_index]) == 1:
        break

oxy_num = int(sorted_lines[top_index:bottom_index][-1],2)

top_index = 0
bottom_index = len(sorted_lines)
for bit in range(num_digits):
    # print("b {}: [{}:{}]".format(bit, top_index, bottom_index))
    # Find the split point
    for i in range(top_index, bottom_index):
        # Looking for the first bit set to 1.
        if sorted_lines[i][bit] == '1':
            # Are we closer to the bottom?
            distance_to_top = i - top_index
            distance_to_bottom = bottom_index - i
            if distance_to_top > distance_to_bottom:
                # Then 0s are more prevelant, reset top to here
                # and run the loop on the next bit.
                top_index = i
                break
            else:
                # Then 0s are more prevelant reset bottom to here
                bottom_index = i
                break
    if len(sorted_lines[top_index:bottom_index]) == 1:
        break
co2_num = int(sorted_lines[top_index:bottom_index][0],2)

print(oxy_num * co2_num)
