#!/usr/bin/env python3

from planet import *

anin = Planet()
anin.add_path(((16, 4), Direction.EAST),
                    ((17, 4), Direction.WEST), 1)
anin.add_path(((17, 4), Direction.SOUTH),
                    ((17, 2), Direction.NORTH), 2)
anin.add_path(((17, 2), Direction.EAST),
                    ((18, 4), Direction.WEST), 3)
anin.add_path(((18, 4), Direction.NORTH),
                    ((18, 6), Direction.SOUTH), 5)
anin.add_path(((18, 7), Direction.SOUTH),
                    ((18, 6), Direction.NORTH), 1)
anin.add_path(((18, 6), Direction.EAST),
                    ((18, 7), Direction.WEST), 2)
anin.add_path(((18, 7), Direction.WEST),
                    ((16, 7), Direction.EAST), 1)
anin.add_path(((16, 7), Direction.WEST),
                    ((15, 6), Direction.NORTH), 38)
anin.add_path(((16, 7), Direction.SOUTH),
                    ((16, 6), Direction.NORTH), 36)
anin.add_path(((16, 6), Direction.WEST),
                    ((15, 6), Direction.EAST), 2)
print(anin.shortest_path((16, 4), (15, 6)))
