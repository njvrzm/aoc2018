from heapq import heappush, heappop
import re
import string
import sys

job_time = lambda L:string.ascii_uppercase.index(L) + 61

extract = re.compile('Step ([A-Z]).*step ([A-Z])').findall
all_steps = set()
blocked_by = dict()
for [(before, after)] in map(extract, open(sys.argv[1])):
    blocked_by.setdefault(after, set()).add(before)
    all_steps.update({before, after})

ready_later = list()
for step in all_steps:
    if step not in blocked_by:
        heappush(ready, (0, step))

ready_now = list()

worker_ready_at = {i:0 for i in range(5)}

done = list()
worker_work = {i:[] for i in range(5)}
while ready_now or ready_later:
    worker, worker_time = min(worker_ready_at.items(), key = lambda w_t:w_t[1])
    while True:
        (job_time, job) = heappop(ready)
        if job_time < worker_time:
            heappush(ready_now, job)
        else:
            heappush(ready_later, job)
            break

    if ready_now:
        job = heappop(ready_now)
        worker_ready_at[worker] += job_time(job)
    else:
        start, job = heappop(ready_later)
        worker_ready_at[worker] += start + job_time(job)

    for blocked, blockers in list(blocked_by.items()):
        blockers.discard(job)
        if not blockers:
            blocked_by.pop(blocked)
            heappush(ready, (, blocked))
    done.append(job)

print(done)
print(worker_time)
