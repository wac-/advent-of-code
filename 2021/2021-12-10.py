part1_scores: dict[str,int] = {')': 3, ']': 57, '}': 1197, '>': 25137}
part2_scores: dict[str,int] = {')': 1, ']': 2,  '}': 3,    '>': 4}

def ProcessLine(line: str) -> tuple[int, int]:
    stack: list[str] = []
    for char in line:
        match char:
            case '(':
                stack.append(')')
            case '[':
                stack.append(']')
            case '{':
                stack.append('}')
            case '<':
                stack.append('>')
            case _:
                expected = stack.pop()
                if char != expected:
                    return (part1_scores[char], 0)
    part2_score: int = 0
    while stack:
        part2_score *= 5
        part2_score += part2_scores[stack.pop()]
    return (0, part2_score)


with open('2021-12-10.txt') as f:
    sum_error:int = 0
    part2_list: list[int] = []
    for line in f:
        part1_score, part2_score = ProcessLine(line.strip())
        sum_error += part1_score
        if part2_score:
            part2_list.append(part2_score)

print('Part 1: {}'.format(sum_error))
print('Part 2: {}'.format(sorted(part2_list)[len(part2_list) // 2]))
