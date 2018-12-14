import sys

class Goblin:
    aims = {
        'v': (1, 0),
        '>': (0, 1),
        '^': (-1, 0),
        '<': (0, -1)
    }

    def __init__(self, y, x, aim):
        self.y, self.x = y, x
        self.dy, self.dx = self.aims[aim]
        self.choices = 0

    def advance(self):
        self.check_turn()
        self.y += self.dy
        self.x += self.dx

    def left(self):
        self.dy, self.dx = -self.dx, self.dy

    def right(self):
        self.dy, self.dx = self.dx, -self.dy

    def check_turn(self):
        here = cavern.get((self.y, self.x))
        if here == '+':
            if self.choices == 0:
                self.left()
            elif self.choices == 2:
                self.right()
            self.choices = (self.choices + 1) % 3
        elif here == '/':
            self.right() if self.dy else self.left()
        elif here == '\\':
            self.left() if self.dy else self.right()

    @property
    def where(self):
        return self.y, self.x

    def __lt__(self, other):
        return self.y < other.y or self.y == other.y and self.x < other.x

    def __repr__(self):
        return '<Goblin {0.y}y {0.x}x>'.format(self)


cavern = dict()
goblins = set()

for y, line in enumerate(open(sys.argv[1])):
    for x, character in enumerate(line):
        if character == ' ':
            continue
        if character in Goblin.aims:
            goblins.add(Goblin(y, x, character))
            character = '-' if character in ('>', '<') else '|'
        cavern[(y, x)] = character


first = True
while len(goblins) > 1:
    for goblin in sorted(goblins):
        goblin.advance()
        others = goblins - {goblin}
        victim = next((g for g in others if g.where == goblin.where), None)
        if victim:
            if first:
                print("First crash: {}".format(goblin))
                first = False
            goblins.remove(victim)
            goblins.remove(goblin)
print("Last uncrashed: {}".format(goblins.pop()))
