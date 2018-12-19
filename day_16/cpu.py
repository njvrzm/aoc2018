import operator

class CPU:
    opera = {
        'add': operator.add,
        'ban': operator.and_,
        'bor': operator.or_,
        'set': lambda a,b: a,
        'mul': operator.mul,
        'gt': operator.gt,
        'eq': operator.eq,
    }
    names = {'addr', 'addi', 'mulr', 'muli',
             'bani', 'banr', 'bori', 'borr',
             'setr', 'seti', 'gtir', 'gtri',
             'gtrr', 'eqir', 'eqri', 'eqrr'}
    indirect_as = {'gt', 'eq', 'set'}

    def __init__(self):
        self.load()

    def load(self, register = None):
        self.reg = list(register or [0] * 4)

    def apply(self, opname, a, b, c):
        for name, op in self.opera.items():
            if opname.startswith(name):
                break
        else:
            raise ValueError("Unknown operator: {}".format(opname))

        if not (name in self.indirect_as and opname.startswith(name + 'i')):
            a = self.reg[a]
        if opname.endswith('r'): # false positive for set, but no matter
            b = self.reg[b]
        self.reg[c] = int(op(a, b))
