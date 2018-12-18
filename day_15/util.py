from collections import OrderedDict
from habitors import Habitor

def init(text = None, fn = None):
    if text is None:
        text = open(fn).read()
    scan(text)


def scan(karte):
    grave.clear()
    space.clear()
    locus.clear()
    for y, line in enumerate(karte.splitlines()):
        for x, character in enumerate(line):
            place = (y, x)
            thing = embody(character)
            space[place] = thing
            locus[thing] = place


def neighbors(being):
    y, x = locus[being]
    for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        yield space[y + dy, x + dx]

def living():
    return [being for being in space.values() if being.alive]


def find(me):
    past = set()
    foes = [being for being in locus if being.kind is me.foekind]
    wavefront = sorted(neighbor for foe in foes for neighbor in neighbors(foe)
            if neighbor.kind is Habitor.Space)

    while wavefront:
        beings, wavefront = wavefront, list()
        for being in beings:
            for neighbor in neighbors(being):
                if neighbor is me:
                    return being
                elif neighbor in past:
                    continue
                elif neighbor.kind is Habitor.Space:
                    wavefront.append(neighbor)
                    past.add(neighbor)


def stream(overlay = None):
    overlay = overlay or dict()
    for place in space:
        if place[1] == 0:
            yield '\n'
        yield overlay.get(place, space[place])


def show():
    print(*map(str, stream()), sep='')


def embody(symbol):
    from actors import Actor, Being
    kind = Habitor(symbol)
    if kind in (Habitor.Elf, Habitor.Goblin):
        return Actor(Habitor(symbol))
    else:
        return Being(Habitor(symbol))

def swap(me, you):
    space[locus[me]], space[locus[you]] = you, me
    locus[me], locus[you] = locus[you], locus[me]

locus = dict()
space = OrderedDict()
grave = set()


