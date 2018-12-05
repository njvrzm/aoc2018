from collections import Counter

import datetime
import re
import sys

record = '{timestamp} ({event})'

events = {
    '(?P<sleep>falls asleep)',
    '(?P<wake>wakes up)',
    'Guard #(?P<gid>[0-9]+) (?P<begin>begins shift)'
}

timestamp = r'\[(?P<timestamp>[^]]+)\]'

rx = record.format(timestamp = timestamp, event = '|'.join(events))

time_format = '%Y-%m-%d %H:%M'

def parse(line):
    event = re.match(rx, line).groupdict()
    event['timestamp'] = datetime.datetime.strptime(event['timestamp'], time_format)
    event['gid'] = int(event['gid']) if event['gid'] else None
    return event

class Nap:
    def __init__(self, start):
        self.start = start
        self.end = None
    
    def finish(self, end):
        self.end = end 

    @property
    def done(self):
        return self.end is not None

    def __iter__(self):
        return iter(range(self.start, self.end))

    def __len__(self):
        return self.end - self.start

    def __repr__(self):
        if self.done:
            return '<Nap from {} to {}>'.format(self.start, self.end)
        else:
            return '<Nap ongoing from {}>'.format(self.start)


class Guard:
    def __init__(self, gid):
        self.gid = gid
        self.naps = list()

    def __repr__(self):
        return '<Guard {}>'.format(self.gid)

    @property
    def current_nap(self):
        return self.naps[-1]
    
    @property
    def am_awake(self):
        return not self.naps or self.naps[-1].done

    def sleep(self, when):
        if not self.am_awake:
            raise ValueError("I'm already asleep!")
        self.naps.append(Nap(when.minute))

    def wake(self, when):
        if self.am_awake:
            raise ValueError("I'm already awake!")
        self.current_nap.finish(when.minute)

    def total_sleep(self):
        return sum(len(nap) for nap in self.naps)

    def sleepiest_minute(self):
        if not self.naps:
            return 0, 0
        minute_sleeps = Counter(minute for nap in self.naps for minute in nap)
        [(minute, count)] = minute_sleeps.most_common(1)
        return minute, count


if __name__ == '__main__':
    events = map(parse, open(sys.argv[1]))
    events = sorted(events, key = lambda e:e['timestamp'])

    guards = dict()
    current_guard = None
    for event in events:
        if event['begin']:
            if event['gid'] not in guards:
                guards[event['gid']] = Guard(event['gid'])
            current_guard = guards[event['gid']]
        elif event['sleep']:
            current_guard.sleep(event['timestamp'])
        elif event['wake']:
            current_guard.wake(event['timestamp'])

    sleepy = max(guards.values(), key = lambda g:g.total_sleep())
    consistent = max(guards.values(), key = lambda g:g.sleepiest_minute()[1])

    print("Sleepiest: {}".format(sleepy.gid * sleepy.sleepiest_minute()[0]))
    print("Most consistent: {}".format(consistent.gid * consistent.sleepiest_minute()[0]))



