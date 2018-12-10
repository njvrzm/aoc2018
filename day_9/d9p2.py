import sys
from collections import deque

nelves, nmarbles = map(int, sys.argv[1:])

board = deque([0])

def advance():
    board.append(board.popleft())

def rewind():
    for _ in range(8):
        board.appendleft(board.pop())

insert = board.append
remove = board.popleft

score = {e:0 for e in range(nelves)}

for marble in range(1, nmarbles):
    if marble % 23 != 0:
        advance()
        insert(marble)
    else:
        rewind()
        bonus = remove()
        advance()
        score[marble % nelves] += marble + bonus

print(max(score.values()))
