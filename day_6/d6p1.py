from collections import namedtuple, Counter, defaultdict
import random
import re
import sys

_point = namedtuple('point', ('x', 'y'))

class point(_point):
    def __add__(self, other):
        return point(self.x + other.x, self.y + other.y)


class Locus(point):
    def __new__(cls, index, x, y):
        it = super().__new__(cls, x, y)
        it.index = index
        return it


coords = (map(int, line.split(',')) for line in open(sys.argv[1]))
loci = [Locus(i, *coord) for i, coord in enumerate(coords)]

leftmost = min(locus.x for locus in loci)
rightmost = max(locus.x for locus in loci)
top = min(locus.y for locus in loci)
bottom = max(locus.y for locus in loci)

nowhere = point(0, 0)
up = point(0, -1)
left = point(-1, 0)
down = point(0, 1)
right = point(1, 0)

steps = {up, up, down, down, left, right, left, right}

space = {locus + nowhere:locus.index for locus in loci}
active = list(loci)

infinite = set()
while active:
    new_active = list()
    for locus in active:
        for step in steps:
            neighbor = locus + step
            if neighbor in space:
                continue
            alive = Locus(locus.index, *neighbor)
            space[alive] = locus.index
            if (neighbor.x < leftmost or neighbor.x > rightmost
                    or neighbor.y < top or neighbor.y > bottom):
                infinite.add(locus.index)
            else:
                new_active.append(Locus(locus.index, *neighbor))
    active = new_active

[winner] = Counter(index for point, index in space.items() if index not in infinite).most_common(1)
print(winner)
import string
letters = string.ascii_letters
def random_color():
    return '{}{}{}'.format(*(random.choice('89ABCEF') for _ in range(3)))

colors = defaultdict(random_color)

def lines():
    for y in range(top, bottom + 1):
        row = []
        for x in range(leftmost, rightmost + 1):
            if point(x, y) in space:
                row.append(letters[space[point(x,y)]])
        row = ''.join(row)
        parts = [x[0] for x in re.findall(r'((.)\2*)', row)]
        for part in parts:
            yield '<span style="color:#{}">{}</span>'.format(colors[part[0]], 'O'*len(part))
        yield '\n'




from functools import partial
with open('maaap.html', 'w') as out:
    out.write('<html><div style="white-space: pre; font-family: monospace;font-size: 2px">')

    print(*lines(), file=out, sep='')
    out.write('</div></html>')

