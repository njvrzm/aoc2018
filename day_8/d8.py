class Branch:
    def __init__(self, stream):
        nbranches, nmetas = next(stream), next(stream)
        self.branches = [Branch(stream) for _ in range(nbranches)]
        self.metas = [next(stream) for _ in range(nmetas)]

    @property
    def sum(self):
        return sum(self.metas) + sum(branch.sum for branch in self.branches)

    @property
    def value(self):
        if not self.branches:
            return sum(self.metas)
        return sum(self.branches[meta - 1].value
                for meta in self.metas
                if meta <= len(self.branches))


stream = map(int, open('tree.txt').read().split())

tree = Branch(stream)
print(tree.sum)
print(tree.value)
