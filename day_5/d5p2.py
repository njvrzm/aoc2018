import sys
import string
from util import react

polymer = open(sys.argv[1]).read().strip()
for letter in string.ascii_lowercase:
    print('{}\t{}'.format(letter, len(react(list(filter(lambda c:c.lower()!=letter, polymer))))))

