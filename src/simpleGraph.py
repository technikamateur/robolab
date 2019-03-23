#!/usr/bin/env python3
from collections import OrderedDict
import logging


class SimpleGraph:
    def __init__(self, nodes, start, target):
        self.logger = logging.getLogger('SimpleGraph')
        logging.basicConfig(level=logging.DEBUG)
        self.nodes = []
        self.start = start
        self.target = target
        for element in nodes:
            # remove loops
            if element[0] == element[1]:
                self.logger.info("Detected loop:")
                self.logger.info(element)
            else:
                self.nodes.append(element)
        """
        nodes looks like:

        start   Target  Weight
        ----------------------
        (0,1)   (1,0)   2
        """

    def printAll(self):
        for element in self.nodes:
            print(element)

    def pathPossible(self):
        containsStart = False
        containsTarget = False
        for edge in self.nodes:
            if edge[0] == self.start:
                containsStart = True
            if edge[0] == self.target:
                containsTarget = True
        if containsStart and containsTarget:
            self.logger.info("Start and target are an element of planet")
            return True
        else:
            self.logger.warning(
                "Start and target are NOT an element of planet")
            return False

    def dijkstra(self):
        # paths with same weight is still a problem...
        startNode = [None, self.start, 0]
        currentNode = startNode
        shortestPath = []
        availablePaths = []
        usedNodes = []  # conatins nodes already have been used
        shortestPath.append(startNode)
        usedNodes.append(startNode[1])
        while currentNode[1] != self.target:
            weights = []
            # add possible paths to availablePaths - but only unused
            for edge in self.nodes:
                if currentNode[1] == edge[0] and not (edge[1] in usedNodes):
                    newWeightEdge = edge
                    newWeightEdge[2] += currentNode[2]
                    availablePaths.append(newWeightEdge)
            # if there are no availablePaths target is not reachable
            if not availablePaths:
                return None
            # add here cleaning if same edges with diffrent weigths exist
            availablePaths = listCleaning(availablePaths)
            # find the shortest of them
            for edge in availablePaths:
                weights.append(edge[2])
            # get the index of smallest
            shortestWay = weights.index(min(weights))
            # move from availablePaths to shortestPath
            shortestPath.append(availablePaths[shortestWay])
            del availablePaths[shortestWay]
            # make latest shortest node to currentNode
            currentNode = shortestPath[-1]
            usedNodes.append(shortestPath[-1][1])
            # remove all elements from availablePaths containing
            # a node from usedNodes as targets
            for edge in availablePaths:
                if edge[1] in usedNodes:
                    availablePaths.remove(edge)
        shortestPath = shortestPathFormatter(shortestPath)
        return shortestPath


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


def shortestPathFormatter(path):
    # reverse list
    path.reverse()
    del path[-1]
    # setting up some vthings
    newShortestPath = []
    nextTarget = None
    for edge in path:
        if nextTarget == None:
            nextTarget = edge[0]
            newShortestPath.append(edge)
        elif edge[1] == nextTarget:
            nextTarget = edge[0]
            newShortestPath.append(edge)
        else:
            pass
    newShortestPath.reverse()
    return newShortestPath
