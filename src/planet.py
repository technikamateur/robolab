#!/usr/bin/env python3

from enum import Enum, unique
from typing import List, Optional, Tuple, Dict

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
    Contains the representation of the map and provides certain functions to manipulate it according to the specifications
    """

    def __init__(self):
        """ Initializes the data structure """
        self.target = None
        self.paths = {}
        self.weights = {}


# ((a, b), c)
# start[1]
#d.update({key:value})

    def add_path(self, start: Tuple[Tuple[int, int], Direction],
                 target: Tuple[Tuple[int, int], Direction], weight: int):
        """
         Adds a bidirectional path defined between the start and end coordinates to the map and assigns the weight to it
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
                destination = {start[1]: [target[0], target[1], weight]}
                self.paths[start[0]].update(destination)

            else:
                # add node to dict
                destination = {}
                destination.update({start[1]: [target[0], target[1], weight]})
                self.paths.update({start[0]: destination})
        elif weight == -1:
            # if path is blocked
            pass
        else:
            print("Ooops. Die Pfadangabe war nicht korrekt!")

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

    def OLDshortest_path(self, start: Tuple[int, int], target: Tuple[int, int]
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
        shortestPath = []
        currentNode = start
        availablePaths = []
        while currentNode != target:
            # I can reach these nodes
            destinations = self.paths.get(currentNode).items()
            # all paths are added to availablePaths
            for element in destinations:
                availablePaths.append(element)
            weights = []
            # now find the smallest element, remove from available and add to shortestPath
            for element in availablePaths:
                weights.append[element[1][2]]
            smallestWay = weigths.index(min(weights))
            # add to shortestPath remove from availablePaths
            shortestPath.append(availablePaths[smallestWay])
            del availablePaths[smallestWay]
            currentNode = shortestPath[-1]

            # First element is shortest
            currentShortestPath.append(destinations[0])
            # Get the real first element
            for element in destinations:
                if element[1][2] < currentShortestPath[1][2]:
                    del currentShortestPath[-1]
                    currentShortestPath.append(element[1][2])
                else:
                    pass
            # Add other paths to buffer
            for element in destinations:
                if element != currentShortestPath[-1]:
                    availablePaths.append(element)
                else:
                    pass



            print("Ich habe es versucht...")
            currentNode = target

        return None


        # shortest paths is a dict of nodes
        # whose value is a tuple of (previous node, weight)
        # shortest_paths = {start: (None)}
        # current_node = start
        # visited = set()
        #
        # while current_node != target:
        #     visited.add(current_node)
        #     destinations = self.paths.get(currentNode).items()
        #     if shortest_paths[current_node] == None:
        #         weight_to_current_node = 0
        #     else:
        #         weight_to_current_node = shortest_paths[current_node][1][2]
        #     # Bis hier top
        #     for next_node in destinations:
        #         weight = self.weights[(current_node, next_node)] + weight_to_current_node
        #         if next_node not in shortest_paths:
        #             shortest_paths[next_node] = (next_node)
        #         else:
        #             current_shortest_weight = shortest_paths[next_node][1]
        #             if current_shortest_weight > weight:
        #                 shortest_paths[next_node] = (current_node, weight)
        #
        #     next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
        #     if not next_destinations:
        #         return "Route Not Possible"
        #     # next node is the destination with the lowest weight
        #     current_node = min(next_destinations, key=lambda k: next_destinations[k][1])
        #
        # # Work back through destinations in shortest path
        # path = []
        # while current_node is not None:
        #     path.append(current_node)
        #     next_node = shortest_paths[current_node][0]
        #     current_node = next_node
        # # Reverse path
        # path = path[::-1]
        # return path
