class Branch:
    def __init__(self, stream):
        nbranches, nmetas = next(stream), next(stream)
        self.branches = [Branch(stream) for _ in range(nbranches)]
        self.metas = [next(stream) for _ in range(nmetas)]

    @property
    def transmetas(self):
        for meta in self.metas:
            yield meta
        for branch in self.branches:
            yield from branch.transmetas

stream = map(int, open('tree.txt').read().split())

print(sum(Branch(stream).transmetas))


