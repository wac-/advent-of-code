
initial: str = ''
replacement: dict[str, str] = {}

with open('2021-12-14.txt') as f:
    for line in (l.strip() for l in f):
        if '->' in line:
            pair, insert = (x.strip() for x in line.split('->'))
            replacement[pair] = pair[0] + insert
        elif line:
            initial = line

line = initial
for i in range(10):
    next_line: str = ''
    for c in range(len(line)-1):
        next_line += replacement[line[c:c+2]]
    next_line += line[-1]

    line = next_line

elements = set(line)
element_count: dict[str, int] = {}
for element in elements:
    element_count[element] = line.count(element)

print(f'{len(line)} = '
      f'{max(element_count.values()) - min(element_count.values())}')