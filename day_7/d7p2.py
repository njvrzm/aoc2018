from entities import Worker, Job
from util import read_jobs

jobs = read_jobs()
workers = [Worker() for _ in range(5)]

while jobs:
    todo = min(jobs, key = Job.priority)
    doer = min(workers, key = Worker.ready_at)
    doer.do(todo)
    jobs.remove(todo)

print(max(worker.busy_until for worker in workers))