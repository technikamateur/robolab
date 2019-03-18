#!/usr/bin/env python3

from enum import Enum, unique
from typing import List, Optional, Tuple, Dict
from simpleGraph import SimpleGraph
import logging

# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE


@unique
class Direction(Enum):
    """ Directions in degrees """
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"


# simple alias, no magic here
Weight = int
"""
    Weight of a given path (received from the server)
    value:  -1 if blocked path
            >0 for all other paths
            never 0
"""


class Planet:
    """
    Contains the representation of the map and provides certain functions
    to manipulate it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.paths = {}
        self.weights = {}
        self.graph = None
        self.impossibleTarget = None
        # creating logger
        self.logger = logging.getLogger('Planet')
        logging.basicConfig(level=logging.DEBUG)


# ((a, b), c)
# start[1]
#d.update({key:value})

    def add_path(self, start: Tuple[Tuple[int, int], Direction],
                 target: Tuple[Tuple[int, int], Direction], weight: int):
        """
         Adds a bidirectional path defined between the start and end
         coordinates to the map and assigns the weight to it
        example:
            add_path(((0, 3), Direction.NORTH), ((0, 3), Direction.WEST), 1)
        :param start: 2-Tuple
        :param target:  2-Tuple
        :param weight: Integer
        :return: void
        """
        if weight > 0:
            if start[0] in self.paths:
                # node in dict
                self.paths[start[0]].update({
                    start[1]: (target[0], target[1], weight)
                })

            elif start[0] not in self.paths:
                # add node to dict
                self.paths.update({
                    start[0]: {
                        start[1]: (target[0], target[1], weight)
                    }
                })

            if target[0] in self.paths:
                # node in dict
                self.paths[target[0]].update({
                    target[1]: (start[0], start[1], weight)
                })

            elif target[0] not in self.paths:
                # add node to dict
                self.paths.update({
                    target[0]: {
                        target[1]: (start[0], start[1], weight)
                    }
                })

        elif weight == -1:
            # if path is blocked
            # I can not remember path is blocked or not, after scanning node again
            self.logger.warn("Path is blocked:")
            self.logger.warn(start)
            pass
        else:
            self.logger.error("Path could not be added!")

        if self.impossibleTarget is not None:
            self.logger.error("There are unfound targets. Implement it now!")

    def get_paths(
            self
    ) -> Dict[Tuple[int, int],
              Dict[Direction, Tuple[Tuple[int, int], Direction, Weight]]]:
        """
        Returns all paths
        example:
            get_paths() returns:
            {
                (0, 3): {
                    Direction.NORTH: ((0, 3), Direction.WEST, 1),
                    Direction.EAST: ((1, 3), Direction.WEST, 2)
                },
                (1, 3): {
                    Direction.WEST: ((0, 3), Direction.EAST, 2),
                    ...
                },
                ...
            }
        :return: Dict
        """
        return self.paths

    def shortest_path(self, start: Tuple[int, int], target: Tuple[int, int]
                      ) -> Optional[List[Tuple[Tuple[int, int], Direction]]]:
        """
        Returns a shortest path between two nodes
        examples:
            shortest_path((0,0), (2,2)) returns: [((0, 0), Direction.EAST), ((1, 0), Direction.NORTH)]
            shortest_path((0,0), (1,2)) returns: None
        :param start: 2-Tuple
        :param target: 2-Tuple
        :return: List, Direction
        """
        # check that start and target is part of graph
        # problem start or target does not have to be part of self.paths.keys
        #if not (start in self.paths and target in self.paths):
        #    return None
        self.logger.info("Shortest path requested")
        # create graph or regen graph
        self.logger.info("Performing graph creation...")
        graphList = []
        for key, value in self.paths.items():
            for targets in value.values():
                edge = [key, targets[0], targets[2]]
                graphList.append(edge)
        self.graph = SimpleGraph(graphList, start, target)
        self.logger.info("...done.")

        if self.graph.pathPossible() == True:
            self.logger.info("Path valid - returning shortest path now.")
            self.graph.printAll()
            # get the path and add directions
            shortestPath = []
            pathExDirection = self.graph.dijkstra(start, target)
            pathExDirection.reverse()
            print(pathExDirection)
            for edge in pathExDirection:
                valueDict = self.paths[edge[0]]
                for keys, values in valueDict.items():
                    if edge[1] in values:
                        shortestPath.append((edge[0], keys))
                        break
                    else:
                        print(edge)
                        pass
            return shortestPath
        else:
            self.logger.warn("Path invalid - saving this")
            self.impossibleTarget = target
            return None
