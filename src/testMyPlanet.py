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
test.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
test.add_path(((0, 0), Direction.SOUTH), ((0, 1), Direction.SOUTH), 2)
test.add_path(((0, 1), Direction.EAST), ((1, 1), Direction.WEST), 3)
test.add_path(((1, 0), Direction.SOUTH), ((1, 1), Direction.NORTH), 6)

pretty(test.get_paths())
print("\n")
print("-------------------------------")
print("\n")
test.shortest_path((0, 0), (1, 1))
