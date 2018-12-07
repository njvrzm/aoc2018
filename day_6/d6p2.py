import random
import sys

coords = [tuple(map(int, line.split(','))) for line in open(sys.argv[1])]

xs = [c[0] for c in coords]
ys = [c[0] for c in coords]

leftmost = min(xs)
rightmost = max(xs)
top = min(ys)
bottom = max(ys)

xds = [0, 1, -1, 0]
yds = [1, 0, 0, -1]


def taxi(a, b):
    ax, ay = a
    bx, by = b
    return abs(bx-ax)+abs(by-ay)

start = (sum(xs)//len(xs), sum(ys)//len(ys))
active = [start]
in_region = {start}
out_region = set()

while active:
    new_active = list()
    for x, y in active:
        for xd, yd in zip(xds, yds):
            where = x+xd, y+yd
            if where in in_region or where in out_region:
                continue
            total = sum(taxi(where, coord) for coord in coords)
            if total < 10000:
                new_active.append(where)
                in_region.add(where)
            else:
                out_region.add(where)
                
    active = new_active

#print(in_region, out_region)

def lines():
    for y in range(top, bottom + 1):
        row = []
        for x in range(leftmost, rightmost + 1):
            if (x, y) in coords:
                row.append('-')
            elif (x,y) in in_region:
                row.append('O')
            elif (x,y) in out_region:
                row.append('.')
            else:
                row.append(' ')
        yield ''.join(row)



print(len(in_region))

from functools import partial
with open('safe.html', 'w') as out:
    out.write('<html><div style="white-space: pre; font-family: monospace;font-size: 2px">')

    print(*lines(), file=out, sep='\n')
    out.write('</div></html>')

