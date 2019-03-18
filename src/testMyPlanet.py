#!/usr/bin/env python3
from planet import Planet, Direction
import pprint
from collections import OrderedDict
import time


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


start = time.time()
test = Planet()
print("Planet Doctor Strange")
test.add_path(((0, 0), Direction.NORTH), ((0, 1), Direction.SOUTH), 50)
test.add_path(((0, 1), Direction.NORTH), ((1, 2), Direction.WEST), 70)
test.add_path(((1, 2), Direction.SOUTH), ((2, 0), Direction.WEST), 120)
test.add_path(((2, 0), Direction.NORTH), ((2, 2), Direction.SOUTH), 100)
test.add_path(((2, 2), Direction.NORTH), ((2, 2), Direction.WEST), 100)
test.add_path(((2, 2), Direction.EAST), ((3, 2), Direction.WEST), 50)
test.add_path(((3, 2), Direction.EAST), ((4, 1), Direction.NORTH), 70)
test.add_path(((3, 2), Direction.SOUTH), ((4, 1), Direction.WEST), 150)
test.add_path(((4, 1), Direction.SOUTH), ((4, 0), Direction.NORTH), 50)
test.add_path(((4, 1), Direction.EAST), ((4, 0), Direction.EAST), 70)
test.add_path(((4, 0), Direction.WEST), ((2, 0), Direction.EAST), 100)

pretty(test.get_paths())
print("\n")
print("-------------------------------")
print("Der kürzeste Pfad lautet:")
print(test.shortest_path((0, 0), (4, 1)))
end = time.time()
print(end - start)
