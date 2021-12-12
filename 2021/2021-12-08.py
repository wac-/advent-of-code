from collections import defaultdict

# Upper-case positions from this chart:
#  AAA
# B   C
#  DDD
# E   F
#  GGG

segment_counts: list[tuple[int,tuple[str, ...]]] = [
    (6, ('A', 'B', 'C',      'E', 'F', 'G')),
    (2, (          'C',           'F'     )),  ##
    (5, ('A',      'C', 'D', 'E',      'G')),
    (5, ('A',      'C', 'D',      'F', 'G')),
    (4, (     'B', 'C', 'D',      'F'     )),  ##
    (5, ('A', 'B',      'D',      'F', 'G')),
    (6, ('A', 'B',      'D', 'E', 'F', 'G')),
    (3, ('A',      'C',           'F'     )),  ##
    (7, ('A', 'B', 'C', 'D', 'E', 'F', 'G')),  ##
    (6, ('A', 'B', 'C', 'D',      'F', 'G')),
]

lit_segment_counts: defaultdict[int, int] = defaultdict(lambda: 0)

def ReturnMatchingDigit(lit_segments: tuple[str, ...]) -> int:
    for i in range(len(segment_counts)):
        if segment_counts[i][1] == lit_segments:
            return i
    raise IndexError('wtf lit segments: {}'.format(lit_segments))

def PossibleDigits(lit_segments: int) -> list[int]:
    possible: list[int] = []
    for i in range(len(segment_counts)):
        if segment_counts[i][0] == lit_segments:
            possible.insert(-1, i)
    return possible

def SortLetterGroups(letters: str) -> str:
    groups: list[str] = [''.join(sorted(g)) for g in letters.strip().split(' ')]
    return ' '.join(groups)

with open('2021-12-08.txt') as f:
    output_sum = 0
    for line in f:
        # Mapping from supplied positions to the set of possible physical positions.
        # e.g. if "a" could be A, B, or C: positions['a'] -> {'A','B','C'}
        positions: dict[str, set[str]] = {}
        for pos in ('abcdefg'):
            positions[pos] = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}

        digit_combinations, display_digits = line.strip().split('|')
        digit_combinations = SortLetterGroups(digit_combinations)
        display_digits = SortLetterGroups(display_digits)

        # Count segments for part 1
        for digit in display_digits.split(' '):
            lit_segment_counts[len(digit)] += 1
        
        # Decode the combinations for part 2
        # We know 1, 4, 7, 8 are unique.
        # Mark the letters with the segments they could possibly be.
        for digit in digit_combinations.strip().split(' '):
            if not digit: continue
            lit_segments = len(digit)

            # Which digits could this digit be?
            possible: list[int] = PossibleDigits(lit_segments)
            
            # If there's only one possible digit here, that eliminates other segments
            # as possible participants in this digit.
            possible_segments: set[str] = set()
            required_segments: set[str] = {'A', 'B', 'C', 'D', 'E', 'F', 'G'}
            for possibility in possible:
                possible_segments = possible_segments.union(
                    set(segment_counts[possibility][1])
                )
                if not required_segments:
                    required_segments = set(segment_counts[possibility][1])
                else:
                    required_segments.intersection_update(set(segment_counts[possibility][1]))
            for segment in positions:
                if segment in digit:
                    # If it's lit, narrow to one of our known segments
                    positions[segment] = positions[segment].intersection(
                        possible_segments
                    )
                elif segment not in digit:
                    # If it's not lit, it can't be required by all possible digits here.
                    positions[segment] = positions[segment].difference(
                        required_segments
                    )

        # Now we have enough to assemble the final mapping.
        mapping: dict[str, str] = {}
        for k in positions:
            # After this logic, we always get G as {E,G} and F as {F,C}.
            if len(positions[k]) == 2:
                if 'G' in positions[k]:
                    mapping[k] = 'G'
                elif 'F' in positions[k]:
                    mapping[k] = 'F'
            else:
                mapping[k] = positions[k].pop()

        # Now we can translate the display digits
        output_int = 0
        for digit in display_digits.strip().split(' '):
            mapped_digit = ''
            # Apply the mapping.
            for segment in digit:
                mapped_digit += mapping[segment]
            lit_segment_tuple = tuple(sorted(mapped_digit))
            digit_int = ReturnMatchingDigit(lit_segment_tuple)
            output_int = output_int * 10 + digit_int
        output_sum += output_int
    print('Part 2: {}'.format(output_sum))



#for key in sorted(lit_segment_counts.keys()):
#    print('{} segs: {}'.format(key, lit_segment_counts[key]))

print('Part 1: {}'.format(sum(lit_segment_counts[segment_counts[i][0]] for i in (1,4,7,8))))