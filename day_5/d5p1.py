import sys
from util import react
polymer = open(sys.argv[1]).read().strip()
print(len(react(polymer)))
