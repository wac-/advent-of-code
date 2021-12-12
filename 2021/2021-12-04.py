from typing import Tuple

part_one = False

Board = Tuple[25 * (int,)]

with open('2021-12-04.txt') as f:
    bingo_numbers: list[int] = [int(n) for n in f.readline().split(',')]

    # Boards are stored as List[int] row-wise.
    boards: list[Board] = []

    # Now consume Bingo boards.
    while True:
        this_board: list[int] = []
        for i in range(6):
            this_line = [int(i) for i in f.readline().strip().split(' ') if i != '']
            # print("l: {}".format(this_line))
            this_board += this_line
        # print("b: {}".format(this_board))
        if not this_board: 
            # We've hit EOF.
            break
        assert(len(this_board) == 25)
        boards.append(tuple(this_board))

print("b_n: {}".format(list(bingo_numbers)))
print("boards:")
for board in boards:
    print("  [{}]: {}".format(len(board), board))

def IsBoardWinner(numbers: list[int], board: list[int]) -> bool:
    board_called = [True if n in numbers else False for n in board]
    # Look for horizontal winners.
    for row in range(5):
        if all(board_called[5*row:5*row+5]):
            return True
    # Look for vertical winners
    for col in range(5):
        if all(board_called[col::5]):
            return True
    return False

# Look for winners one at a time.
winning_board: list[int] = []
winning_number: int = 0
uncalled_numbers: list[int] = []
for i in range(len(bingo_numbers)):
    for board in boards:
        if IsBoardWinner(bingo_numbers[:i], board):
            winning_board = board
            winning_number = bingo_numbers[i-1]
            # Find uncalled numbers on board.
            uncalled_numbers = [n for n in winning_board if n not in bingo_numbers[:i]]
            if part_one: break
            else:
                boards.remove(board)
    if (part_one and winning_board) or not boards:
        break

print("Winning board: {}".format(winning_board))
print("Sum uncalled: {}".format(sum(uncalled_numbers)))
print("Winning number: {}".format(winning_number))
print("Score: {}".format(winning_number * sum(uncalled_numbers)))