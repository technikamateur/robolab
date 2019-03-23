#!/usr/bin/env python3

from planet import *

havok = Planet()

havok.add_path(((15, 37), Direction.NORTH), ((15, 39), Direction.SOUTH), 1)
havok.add_path(((15, 37), Direction.EAST), ((17, 37), Direction.WEST), 1)
havok.add_path(((15, 39), Direction.NORTH), ((15, 39), Direction.WEST), 1)
havok.add_path(((15, 39), Direction.EAST), ((16, 39), Direction.WEST), 1)
havok.add_path(((16, 39), Direction.EAST), ((17, 38), Direction.NORTH), 1)
havok.add_path(((16, 39), Direction.SOUTH), ((17, 38), Direction.WEST), 1)
havok.add_path(((17, 38), Direction.SOUTH), ((17, 37), Direction.NORTH), 1)
havok.add_path(((17, 38), Direction.EAST), ((17, 37), Direction.EAST), 1)
havok.add_path(((15, 37), Direction.WEST), ((14, 39), Direction.SOUTH), 1)
havok.add_path(((14, 39), Direction.WEST), ((13, 38), Direction.NORTH), 1)
havok.add_path(((13, 38), Direction.SOUTH), ((13, 37), Direction.NORTH), 1)

havok.add_unknown_paths({(13, 37): [(Direction.SOUTH, -2)]})
havok.add_unknown_paths({(16, 39): [(Direction.NORTH, -2)]})

print("We are on 13,37 now")
print("Where to go..")
havok.go_direction((13, 37))
print(havok.get_direction((13, 37)))
havok.add_path(((13, 37), Direction.SOUTH), ((13, 37), Direction.SOUTH), -1)
print("Dicovered 13,37. Where to go...")
havok.go_direction((13, 37))
print(havok.get_next_node((13, 37)))


# {
#     (0, 3): {
#         Direction.NORTH: ((0, 3), Direction.WEST, 1),
#         Direction.EAST: ((1, 3), Direction.WEST, 2)
#     },
#     (1, 3): {
#         Direction.WEST: ((0, 3), Direction.EAST, 2),
#         ...
#     },
#     ...
# }
