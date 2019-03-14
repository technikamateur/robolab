#!/usr/bin/env python3
from planet import Planet, Direction
test = Planet()
test.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
test.add_path(((0, 0), Direction.WEST), ((0, 3), Direction.SOUTH), 1)

test.add_path(((0, 2), Direction.NORTH), ((1, 0), Direction.SOUTH), 2)

print(test.getBilloPaths())
