from heapq import heappush, heappop
import re
import sys

extract = re.compile('Step ([A-Z]).*step ([A-Z])').findall
all_steps = set()
blocked_by = dict()
for [(before, after)] in map(extract, open(sys.argv[1])):
    blocked_by.setdefault(after, set()).add(before)
    all_steps.update({before, after})

ready = list()
for step in all_steps:
    if step not in blocked_by:
        heappush(ready, step)

done = list()
while ready:
    do_next = heappop(ready)
    for blocked, blockers in list(blocked_by.items()):
        blockers.discard(do_next)
        if not blockers:
            blocked_by.pop(blocked)
            heappush(ready, blocked)
    done.append(do_next)

print(''.join(done))
