#!/usr/bin/env python3

from enum import Enum, unique
from typing import List, Optional, Tuple, Dict
from simpleGraph import SimpleGraph
from searchable_graph import SearchableGraph
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
        """
        self.unknownPaths looks like
        {
            (0, 0): [Direction.NORTH, Direction.SOUTH, ...]
        }
        """
        self.scannedNodes = set()
        self.unseenNodes = []
        self.graph = None
        # creating logger
        self.logger = logging.getLogger('Planet')
        logging.basicConfig(level=logging.DEBUG)


# ((a, b), c)
# start[1]
#d.update({key:value})

# adds unknown paths

    def add_unknown_paths(self, node):
        """node should look like:
        {
            currentNode: [(Direction.NORTH, -2), (Direction.EAST, -3)]
        } Definition: -1 = blocked, -2 = pathAvailable, -3 = noPath
        """
        key = list(node.keys())[0]
        unknown_paths = list(node.values())[0]
        # filter list, remove -1 and -3 elements
        unknown_paths = [x for x in unknown_paths if -1 not in x]
        unknown_paths = [x for x in unknown_paths if -3 not in x]
        new_unknown_paths = []
        for element in unknown_paths:
            new_unknown_paths.append(element[0])
        self.scannedNodes.add(key)
        self.unknownPaths.update({key: new_unknown_paths})

    # direction with unknown path for node
    def get_direction(self, node):
        value = self.unknownPaths[node]
        return random.choice(value)

    # returns path to next node from node
    def get_next_node(self, node):
        # maybe there are no paths to discover
        if not self.unknownPaths and not self.unseenNodes:
            self.logger.info("Everything discovered. Finishing exploration.")
            return None
        self.logger.info("Performing graph creation...")
        graphList = {}
        for key, value in self.paths.items():
            for targets in value.values():
                if key in graphList and targets[2] > 0:
                    # node in dict
                    graphList[key].append(targets[0])

                elif key not in graphList and targets[2] > 0:
                    # add node to dict
                    graphList.update({key: [targets[0]]})
        intresting_nodes = list(self.unknownPaths.keys())
        intresting_nodes.extend(self.unseenNodes)
        graph = SearchableGraph(graphList, node, intresting_nodes)
        self.logger.info("...done")
        target = graph.find_next_node()
        if target is not None:
            self.logger.info("Found new target node:")
            self.logger.info(target)
            return self.shortest_path(node, target)
        else:
            self.logger.warning("Function did not exit properly.")
            return None

    # check whether node is already scanned
    def node_scanned(self, node):
        self.clean_unknown_paths()
        if node in self.scannedNodes:
            self.logger.info("Node already scanned.")
            return True
        else:
            self.logger.info("Node unknown. Please scan!")
            return False

    # check whether there are unknown directions for node
    def go_direction(self, node):
        self.clean_unknown_paths()
        if node in self.unknownPaths:
            self.logger.info("Dicover Direction on current Node")
            return True
        else:
            self.logger.info("Go to other node")
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
                if start[1] not in self.paths[start[0]]:
                    self.paths[start[0]].update(
                        {start[1]: (target[0], target[1], weight)})
                    self.logger.info("new path added")

            elif start[0] not in self.paths:
                # add node to dict
                self.paths.update(
                    {start[0]: {
                         start[1]: (target[0], target[1], weight)
                     }})
                self.logger.info("new path added")

            if target[0] in self.paths:
                # node in dict
                if target[1] not in self.paths[target[0]]:
                    self.paths[target[0]].update(
                        {target[1]: (start[0], start[1], weight)})

            elif target[0] not in self.paths:
                # add node to dict
                self.paths.update(
                    {target[0]: {
                         target[1]: (start[0], start[1], weight)
                     }})
        elif weight == -1:
            # if path is blocked
            # I can not remember path is blocked or not, after scanning node again
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
        else:
            self.logger.error("Path could not be added!")

    def clean_unknown_paths(self):
        if self.paths:

            for known_key, known_value in self.paths.items():
                known_directions = known_value.keys()
                # append scannedNodes
                if len(known_directions) == 4:
                    self.scannedNodes.add(known_key)
                if known_key in self.unknownPaths:
                    unknown_directions = self.unknownPaths[known_key]
                    new_unknown_paths = [
                        item for item in unknown_directions
                        if item not in known_directions
                    ]
                    if not new_unknown_paths:
                        self.unknownPaths.pop(known_key, None)
                    else:
                        self.unknownPaths[known_key] = new_unknown_paths
            # regen list of unseenNodes
            # criteria: not already scanned
            # and less than 4 edges
            self.unseenNodes = [
                node for node in self.paths.keys()
                if node not in self.scannedNodes
            ]

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
                if targets[2] > 0:
                    edge = [key, targets[0], targets[2]]
                    graphList.append(edge)
        self.graph = SimpleGraph(graphList, start, target)
        self.logger.info("...done.")

        if self.graph.pathPossible():
            #self.graph.printAll()
            # get the path and add directions
            shortestPath = []
            pathExDirection = self.graph.dijkstra()
            if pathExDirection is not None:
                pathExDirection.reverse()
                for edge in pathExDirection:
                    valueDict = self.paths[edge[0]]
                    weight = {}
                    for keys, values in valueDict.items():
                        if edge[1] in values:
                            weight.update({values[2]: keys})
                    smalles_element = min(weight.items(), key=lambda x: x[0])
                    shortestPath.append((edge[0], smalles_element[1]))
                shortestPath.reverse()
                self.logger.info("Shortest Path:")
                self.logger.info(shortestPath)
                return shortestPath
            else:
                self.logger.warning("Target (currently) not reachable.")
                return None
        else:
            self.logger.warning("Path invalid.")
            return None
