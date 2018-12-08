import string
never = float('inf')

class Job:
    rates = ' ' * 61 + string.ascii_uppercase # too cute?

    def __init__(self, name):
        self.name = name
        self.blockers = set()
        self.done_time = never
        self.cost = self.rates.index(self.name)

    def start_time(self):
        if not self.blockers:
            return 0
        return max(blocker.done_time for blocker in self.blockers)

    def block_on(self, other):
        self.blockers.add(other)

    def finish_at(self, time):
        self.done_time = time

    def priority(self):
        return (self.start_time(), self.name)


class Worker:
    def __init__(self):
        self.busy_until = 0

    def ready_at(self):
        return self.busy_until

    def do(self, job):
        start = max(self.ready_at(), job.start_time())
        if start == never:
            raise ValueError("Tried to never work")
        finish = start + job.cost
        self.busy_until = finish
        job.finish_at(finish)
