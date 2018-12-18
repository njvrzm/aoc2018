from habitors import Habitor
from util import neighbors, space, locus, find, swap, grave

class Being:
    def __init__(self, kind):
        self.kind = kind
        self.health = 0

    def __lt__(self, other):
        return locus[self] < locus[other]

    def __str__(self):
        return self.kind.value

    @property
    def power(self):
        return self.kind.power

    @property
    def alive(self):
        return self.health > 0

    def __repr__(self):
        return '<{} @ {} = {}>'.format(self.kind.name, locus[self], self.health)


class Actor(Being):
    def __init__(self, kind):
        super().__init__(kind)
        self.health = 200

    @property
    def foes(self):
        return list(filter(lambda n:n.kind is self.foekind, neighbors(self)))

    @property
    def foekind(self):
        return self.kind.foe

    def fight(self):
        foes = self.foes
        if foes:
            foe = min(foes, key = lambda foe:(foe.health, locus[foe]))
            foe.wound(self.kind.power)

    def move(self):
        if any(self.foes):
            return
        yon = find(self)
        if yon:
            swap(self, yon)

    def wound(self, power):
        if not self.alive:
            raise ValueError("I'm already dead!")
        self.health -= power
        if not self.alive:
            ghost = Being(Habitor.Space)
            space[locus[self]] = ghost
            locus[ghost] = locus.pop(self)
            grave.add(self)
