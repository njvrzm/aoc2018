from itertools import count
from collections import defaultdict
import time
import sys


ROCK = '#'
SPACE = '.'
GOBLIN = 'G'
ELF = 'E'
karte = defaultdict(lambda:ROCK)

NEIGHBORS = [(-1, 0), (0, -1), (0, 1), (1, 0)] # reading order
class Victory(Exception):
    pass

def neighbors(place):
    y, x = place
    return [(y + dy, x + dx) for dy, dx in NEIGHBORS]

def swap(here, there):
    karte[there], karte[here] = karte[here], karte[there]
    points[there] = points.pop(here)
    actors.remove(here)
    actors.add(there)

def die(actor):
    actors.remove(actor)
    points.pop(actor)
    karte[actor] = SPACE
    if len(set(karte[actor] for actor in actors)) == 1:
        raise Victory

def other(me):
    return ELF if karte[me] == GOBLIN else GOBLIN

actors = set()
points = dict()
victors = set()

for y, line in enumerate(open(sys.argv[1])):
    for x, symbol in enumerate(line.strip()):
        place = (y, x)
        if symbol == ROCK:
            continue
        if symbol in (ELF, GOBLIN):
            actors.add(place)
            points[place] = 200
        karte[place] = symbol

depth, width = y + 1, x + 1

def show(overlay = None):
    overlay = overlay or dict()
    for y in range(depth):
        row = []
        for x in range(width):
            place = y, x
            if place in overlay:
                symbol = overlay[place]
                if isinstance(symbol, int):
                    symbol = str(symbol % 10)
            else:
                symbol = karte.get(place, ROCK)
            row.append(symbol)
        print(''.join(row))

def stink(kind):
    seklas = {me for me in actors if karte[me] == kind}
    punge = dict()
    for depth in count():
        for place in list(seklas):
            seklas.remove(place)
            punge[place] = depth
            for neighbor in neighbors(place):
                if neighbor in punge:
                    continue
                if karte[neighbor] == SPACE:
                    seklas.add(neighbor)
        if not seklas:
            break
    return punge

def move(me):
    foekind = other(me)
    nearby = neighbors(me)
    if any(karte[yon] is foekind for yon in nearby):
        return
    scent = stink(foekind)
    trails = [(scent[neighbor], neighbor) for neighbor in neighbors(me)
            if neighbor in scent]
    if not trails:
        return
    strength, destiny = min(trails)
    swap(me, destiny)
    return destiny

def hit(me, you):
    points[you] -= 3
    if points[you] <= 0:
        die(you)

def fight(me):
    nearby = neighbors(me)
    foekind = other(me)
    foes = [yon for yon in nearby if karte[yon] is foekind]
    if foes:
        if any(karte[foe] == karte[me] for foe in foes):
            raise ValueError('wtf')
        foe = min(foes, key = lambda f:(points[f], f))
        hit(me, foe)
        return foe

complete = [0]
def turn():
    action = dict()
    for actor in list(sorted(actors)):
        if victors:
            break
        if actor not in points:
            # RIP
            continue
        yon = move(actor)
        if yon:
            action[actor] = karte[yon].lower()
        try:
            foe = fight(yon or actor)
        except Victory:
            victors.add(actor)
            action[actor] = '0'

        if foe:
            action[foe] = '*'
    else:
        complete[0] = complete[0] + 1
    show(action)

def go():
    show()
    for rounds in count():
        turn()
        if victors:
            break
        time.sleep(.05)
    show()

    remains = sum(points.values())
    score = complete[0] * remains
    print(rounds, complete[0], remains, score)

if __name__ == '__main__':
    go()
