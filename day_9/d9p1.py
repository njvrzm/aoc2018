from itertools import cycle
import sys

nelfs, narbles = map(int, sys.argv[1:])
elves = list(range(nelfs))

board = [0]
score = {elf:0 for elf in elves}

current = 0 # place, not marble
lb = 0

for elf, marble in zip(cycle(elves), range(1, narbles)):
    if marble % 23 == 0:
        bonus = (current - 7) % len(board)
        score[elf] += marble + board[bonus]
        board = board[:bonus] + board[bonus + 1:]
        current = bonus
    else:
        current = (current + 2) % len(board)
        board = board[:current] + [marble] + board[current:]
#    if marble  == 23*971:
#        import IPython;IPython.embed() # DELETEME

print(max(score.values()))

