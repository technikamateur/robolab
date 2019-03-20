#!/usr/bin/env python3

from enum import Enum, unique
from typing import List, Optional, Tuple, Dict
from simpleGraph import SimpleGraph
import logging
import random

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
        self.paths = {}
        self.unknownPaths = {}
        self.scannedNodes = []
        self.graph = None
        self.impossibleTarget = None
        # creating logger
        self.logger = logging.getLogger('Planet')
        logging.basicConfig(level=logging.DEBUG)


# ((a, b), c)
# start[1]
#d.update({key:value})

    adds unknown paths
    def add_unknown_paths(self, node):
        """node should look like:
        {
            currentNode: [(Direction.NORTH, -2), (Direction.EAST, -3)]
        } Definition: -1 = blocked, -2 = pathAvailable, -3 = noPath
        """
        self.scannedNodes.append(node)
        key = list(node.keys())[0]
        unknown_paths = list(node.values())[0]
        if self.paths != None:
            # get known directions for node
            known_paths = self.paths[key]
            # remove paths which are already known
            unknown_paths = [
                unknown for known in known_paths for unknown in unknown_paths
                if known not in unknown
            ]
            """ Funktion drüber soll das machen
            for direc in known_paths:
                for unknown in unknown_paths:
                    if direc not in element:
                        real_unknown_paths.append(unknown)
                    else:
                        pass
            """
        # remove blocked or not existing paths
        unknown_paths = [
            x for x in unknown_paths if -1 not in x or -3 not in x
        ]
        self.unknownPaths.update({key: unknown_paths})
        # return a random existing exit for node
        return random.choice(unknown_paths)[1]

    # direction with unknown path for node
    def get_direction(self, node):
        pass

    # returns path to next node from node
    def get_next_node(self, node):
        pass

    # check whether node is already scanned
    def node_scanned(self, node):
        if node in self.scannedNodes:
            self.logger.info("Node already scanned.")
            return True
        else:
            self.logger.info("Node unknown. Please scan!")
            return False

    # check whether there ar unknown directions for node
    def go_direction(self, node):
        if node in self.unknownPaths:
            return True
        else:
            return False

    # adds path to dict
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
                self.paths[start[0]].update(
                    {start[1]: (target[0], target[1], weight)})

            elif start[0] not in self.paths:
                # add node to dict
                self.paths.update(
                    {start[0]: {
                         start[1]: (target[0], target[1], weight)
                     }})

            if target[0] in self.paths:
                # node in dict
                self.paths[target[0]].update(
                    {target[1]: (start[0], start[1], weight)})

            elif target[0] not in self.paths:
                # add node to dict
                self.paths.update(
                    {target[0]: {
                         target[1]: (start[0], start[1], weight)
                     }})
            # check the current start and target existence in
            # unknownPaths and remove them
            if start[0] in self.unknownPaths:
                value = self.unknownPaths[start[0]]
                for direc in value:
                    if start[1] == direc[1]:
                        self.logger.info("Path explored. Removing from unknown...")
                        value.remove(direc)
                        break
            elif target[0] in self.unknownPaths:
                value = self.unknownPaths[target[0]]
                for direc in value:
                    if target[1] == direc[1]:
                        self.logger.info("Path explored. Removing from unknown...")
                        value.remove(direc)
                        break
            # now, remove all empty keys
            for node in list(self.unknownPaths.keys()):
                if self.unknownPaths[node] == []:
                    del self.unknownPaths[node]

        elif weight == -1:
            # if path is blocked
            # I can not remember path is blocked or not, after scanning node again
            self.logger.warning("Path is blocked:")
            self.logger.warning(start)
            pass
        else:
            self.logger.error("Path could not be added!")

        if self.impossibleTarget is not None:
            self.logger.error("There are unfound targets. Implement it now!")
        # Now unknown paths should be cleaned

    # returns all paths
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

    # returns hopefully shortest path
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

        if self.graph.pathPossible():
            self.logger.info("Path valid - returning shortest path now.")
            self.graph.printAll()
            # get the path and add directions
            shortestPath = []
            pathExDirection = self.graph.dijkstra()
            pathExDirection.reverse()
            for edge in pathExDirection:
                valueDict = self.paths[edge[0]]
                for keys, values in valueDict.items():
                    if edge[1] in values:
                        shortestPath.append((edge[0], keys))
                        break
                    else:
                        pass
            shortestPath.reverse()
            return shortestPath
        else:
            self.logger.warning("Path invalid - saving this")
            self.impossibleTarget = target
            return None
