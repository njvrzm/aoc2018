from functools import partial
import re
import sys

number = '(?P<{}>-?[0-9]+)'
frame = 'position=< *{}, *{}> velocity=< *{}, *{}>'
names = ('x', 'y', 'vx', 'vy')
rex = frame.format(*map(number.format, names))
parse = lambda line:re.match(rex, line).groupdict()

def beeline(line):
    return {name:int(value) for name, value in parse(line).items()}

bees = list(map(beeline, open(sys.argv[1])))

def width(bees):
    return max(bee['x'] for bee in bees) - min(bee['x'] for bee in bees)

def height(bees):
    return max(bee['y'] for bee in bees) - min(bee['y'] for bee in bees)

def bee_at_time(t, bee):
    return dict(bee, x = bee['x'] + bee['vx'] * t, y = bee['y'] + bee['vy'] * t)

def bees_at_time(t):
    return list(map(partial(bee_at_time, t), bees))

def narrowest_time():
    first_width = width(bees_at_time(0))
    second_width = width(bees_at_time(1))

    shrinkage = first_width - second_width

    steps = first_width // shrinkage
    last_width = None
    for t in range(steps, 0, -1):
        width_at_t = width(bees_at_time(t))
        if last_width and width_at_t > last_width:
            return t + 1
        last_width = width_at_t

def show_bees_at_time(t):
    bees = bees_at_time(t)
    places = [(bee['x'], bee['y']) for bee in bees]
    left = min(x for x, y in places)
    right = max(x for x, y in places)
    top = min(y for x, y in places)
    bottom = max(y for x, y in places)
    for y in range(top, bottom + 1):
        row = []
        for x in range(left, right + 1):
            row.append('*' if (x, y) in places else ' ')
        print(''.join(row))

when = narrowest_time()
show_bees_at_time(when)
print("The time is now {}".format(when))