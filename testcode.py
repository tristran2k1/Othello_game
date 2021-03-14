import itertools
from typing import List, Any

posible_positions = []
for (r, c) in itertools.product(list('12345678'), list('abcdefgh')):
    posible_positions.append(c + r)
print(posible_positions)

