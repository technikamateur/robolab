#!/usr/bin/env python3
from planet import Planet, Direction
import pprint


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


test = Planet()
test.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 1)
test.add_path(((0, 0), Direction.WEST), ((0, 3), Direction.SOUTH), 1)

test.add_path(((0, 2), Direction.NORTH), ((1, 0), Direction.SOUTH), 2)

pretty(test.get_paths())
