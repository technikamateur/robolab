#!/usr/bin/env python3
from planet import Planet, Direction
import pprint
from collections import OrderedDict


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))

def listCleaning(paths):
    newPath = OrderedDict()
    for edge in paths:
        key = (edge[0], edge[1])
        if key not in newPath:
            newPath[key] = edge[2]
        else:
            value = newPath[key]
            if edge[2] < value:
                newPath[key] = edge[2]
            else:
                pass
    newPathList = []
    for key, value in newPath.items():
        newPathList.append([key[0], key[1], value])
    return newPathList


test = Planet()
test.add_path(((0, 0), Direction.EAST), ((1, 0), Direction.WEST), 1)
test.add_path(((0, 0), Direction.SOUTH), ((0, 1), Direction.SOUTH), 2)
test.add_path(((0, 1), Direction.EAST), ((1, 1), Direction.WEST), 3)
test.add_path(((1, 0), Direction.SOUTH), ((1, 1), Direction.NORTH), 6)
test.add_path(((0, 0), Direction.NORTH), ((0, 0), Direction.WEST), 2)

pretty(test.get_paths())
print("\n")
print("-------------------------------")
print("\n")
test.shortest_path((0, 0), (1, 1))
print("\n")
print("-------------------------------")
print("\n")
testpath = [
[0, 0, 5],
[1, 0, 5],
[0, 1, 5],
[0, 0, 3],
[0, 0, 7]
]
print(listCleaning(testpath))
