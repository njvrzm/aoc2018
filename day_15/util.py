from collections import OrderedDict
from habitors import Habitor

locus = dict() # actor -> place
space = OrderedDict() # place -> actor
# By always iterating over space to find things, we can eliminate all
# reading order checks.
grave = set() # slain actors

def begin(text = None, fn = None):
    if text is None:
        text = open(fn).read()
    scan(text)


def scan(karte):
    """ Read the map from the string karte. Populate the thing-to-place
    and place-to-thing maps. Clear the grave, in case of multiple runs."""
    grave.clear()
    space.clear()
    locus.clear()
    for y, line in enumerate(karte.splitlines()):
        for x, symbol in enumerate(line):
            place = (y, x)
            thing = embody(symbol)
            space[place] = thing
            locus[thing] = place


def neighbors(being):
    y, x = locus[being]
    for dy, dx in ((-1, 0), (0, -1), (0, 1), (1, 0)):
        yield space[y + dy, x + dx]


def quick():
    return [being for being in space.values() if being.alive]


def find(me):
    past = set()
    wavefront = list()
    for being in space.values():
        if being.kind is not Habitor.Space:
            continue
        if any(neighbor.kind is me.foekind for neighbor in neighbors(being)):
            wavefront.append(being)

    # wavefront is now the space neighbors of all foes, in reading order.
    # We let them propagate in order into _their_ space neighbors, and so on.
    # The first time we propagate to a space that is neighbor to <me>,
    # that's where <me> wants to go.

    while wavefront:
        beings, wavefront = wavefront, list()
        for being in beings:
            for neighbor in neighbors(being):
                if neighbor is me:
                    # They found me!
                    return being
                elif neighbor in past:
                    # been there, done that
                    continue
                elif neighbor.kind is Habitor.Space:
                    # propagate
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

